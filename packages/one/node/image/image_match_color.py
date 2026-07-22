import math
import torch
from abc import ABC, abstractmethod
from comfy.model_management import get_gpu_device_options, resolve_gpu_device_option
from comfy_api.latest import io
from enum import StrEnum
from typing import Callable, Generic, TypedDict, TypeVar, Unpack, cast

class Method(StrEnum):
	HM = "HM"
	MGD = "MGD"
	MKL = "MKL"
	Reinhard = "Reinhard"
	WCT = "WCT"
	Wavelet = "Wavelet"

class _Inputs(TypedDict):
	device: io.Combo.Type
	image: io.Image.Type
	mask: io.Mask.Type | None
	method: io.Combo.Type
	reference: io.Image.Type
	strength: io.Float.Type

class OneImageMatchColor(io.ComfyNode):
	@classmethod
	def define_schema(cls) -> io.Schema:
		return io.Schema(
			node_id = "OneImageMatchColor",
			display_name = "图像匹配颜色",
			category = "One/图像/滤镜",
			inputs = [
				io.Image.Input(
					id = "image",
					display_name = "图像",
				),
				io.Image.Input(
					id = "reference",
					display_name = "参考图像",
				),
				io.Mask.Input(
					id = "mask",
					display_name = "遮罩",
					optional = True,
				),
				io.Combo.Input(
					id = "method",
					options = Method,
					display_name = "方法",
					default = Method.WCT,
				),
				io.Float.Input(
					id = "strength",
					display_name = "强度",
					default = 0.5,
					min = 0.0,
					max = 1.0,
					step = 0.01,
				),
				io.Combo.Input(
					id = "device",
					options = get_gpu_device_options(),
					display_name = "设备",
					advanced = True,
				),
			],
			outputs = [
				io.Image.Output(
					id = "image",
					display_name = "图像",
				),
			],
		)

	@classmethod
	def execute(cls, **kwargs: Unpack[_Inputs]) -> io.NodeOutput:
		image, reference, mask = kwargs["image"], kwargs["reference"], kwargs.get("mask")
		strength = kwargs["strength"]

		if strength <= 0.0:
			return io.NodeOutput(image)

		device = resolve_gpu_device_option(kwargs["device"])
		if device is not None:
			image = image.to(device)
			reference = reference.to(device)

		if mask is not None:
			mask = mask.to(image.device)

		match kwargs["method"]:
			case Method.HM:
				image = HistogramMatching.apply(image, reference, strength, mask)

			case Method.MGD:
				image = MGDMatching.apply(image, reference, strength, mask)

			case Method.MKL:
				image = MongeKantorovichLinear.apply(image, reference, strength, mask)

			case Method.Reinhard:
				image = ReinhardMatching.apply(image, reference, strength, mask)

			case Method.WCT:
				image = WhiteningColoringTransform.apply(image, reference, strength, mask)

			case Method.Wavelet:
				image = WaveletMatching.apply(image, reference, strength, mask)

			case _:
				pass

		return io.NodeOutput(image)

ColorMatchAlgorithmProfile = TypeVar("ColorMatchAlgorithmProfile")
class ColorMatchAlgorithm(ABC, Generic[ColorMatchAlgorithmProfile]):
	@classmethod
	def apply(cls, image: torch.Tensor, reference: torch.Tensor, strength: float = 0.5, mask: torch.Tensor | None = None) -> torch.Tensor:
		ibatch, _, _, ichannel = image.shape
		rbatch, _, _, rchannel = reference.shape

		if ichannel < rchannel:
			reference = reference[..., :ichannel]
		elif ichannel > rchannel:
			reference = reference[..., torch.arange(ichannel, device = reference.device) % rchannel]

		if ibatch < rbatch:
			reference = reference[:ibatch]
		elif ibatch > rbatch:
			reference = reference[torch.arange(ibatch, device = reference.device) % rbatch]

		iprofile = cls._profile(image)
		rprofile = cls._profile(reference)

		return cls._match(iprofile, rprofile, strength, mask)

	@classmethod
	def _covariance(cls, centered: torch.Tensor) -> torch.Tensor:
		count = centered.shape[1]
		return centered.transpose(1, 2) @ centered / (count - 1)

	@classmethod
	def _eigendecomposition(cls, covariance: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
		return cast(tuple[torch.Tensor, torch.Tensor], torch.linalg.eigh(covariance)) # pyright: ignore[reportUnknownMemberType]

	@classmethod
	def _inverse_square_root(cls, covariance: torch.Tensor) -> torch.Tensor:
		eigval, eigvec = cls._eigendecomposition(covariance)
		return cls._spectrum(eigval, eigvec, lambda eigval: eigval.clamp_min(torch.finfo(eigval.dtype).eps).rsqrt())

	@classmethod
	def _lab_to_rgb(cls, tensor: torch.Tensor) -> torch.Tensor:
		lum = tensor[..., 0]
		lab_a = tensor[..., 1]
		lab_b = tensor[..., 2]

		fy = (lum + 16.0) / 116.0
		fx = fy + lab_a / 500.0
		fz = fy - lab_b / 200.0

		fxcube = fx ** 3
		fycube = fy ** 3
		fzcube = fz ** 3

		whitepoint_x = 0.95047
		whitepoint_y = 1.00000
		whitepoint_z = 1.08883

		epsilon = 216.0 / 24389.0
		kappa = 24389.0 / 27.0

		xf = torch.where(epsilon < fxcube, fxcube, (116.0 * fx - 16.0) / kappa)
		yf = torch.where(epsilon < fycube, fycube, (116.0 * fy - 16.0) / kappa)
		zf = torch.where(epsilon < fzcube, fzcube, (116.0 * fz - 16.0) / kappa)

		x = xf * whitepoint_x
		y = yf * whitepoint_y
		z = zf * whitepoint_z

		red = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
		green = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
		blue = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z

		linear = torch.stack([red, green, blue], -1)
		linear.clamp_min_(0.0)

		rgb = torch.where(
			0.0031308 < linear,
			1.055 * linear ** (1.0 / 2.4) - 0.055,
			12.92 * linear,
		)
		rgb = rgb.clamp_(0.0, 1.0)

		return rgb

	@classmethod
	def _mean(cls, tensor: torch.Tensor) -> torch.Tensor:
		return tensor.mean(1)

	@classmethod
	def _rgb_to_lab(cls, tensor: torch.Tensor) -> torch.Tensor:
		linear = torch.where(0.04045 < tensor, ((tensor + 0.055) / 1.055) ** 2.4, tensor / 12.92)

		red = linear[..., 0]
		green = linear[..., 1]
		blue = linear[..., 2]

		x = 0.4124564 * red + 0.3575761 * green + 0.1804375 * blue
		y = 0.2126729 * red + 0.7151522 * green + 0.0721750 * blue
		z = 0.0193339 * red + 0.1191920 * green + 0.9503041 * blue

		whitepoint_x = 0.95047
		whitepoint_y = 1.00000
		whitepoint_z = 1.08883

		xratio = x / whitepoint_x
		yratio = y / whitepoint_y
		zratio = z / whitepoint_z

		epsilon = 216.0 / 24389.0
		kappa = 24389.0 / 27.0

		fx = torch.where(epsilon < xratio, xratio ** (1.0 / 3.0), (kappa * xratio + 16.0) / 116.0)
		fy = torch.where(epsilon < yratio, yratio ** (1.0 / 3.0), (kappa * yratio + 16.0) / 116.0)
		fz = torch.where(epsilon < zratio, zratio ** (1.0 / 3.0), (kappa * zratio + 16.0) / 116.0)

		lum = 116.0 * fy - 16.0
		lab_a = 500.0 * (fx - fy)
		lab_b = 200.0 * (fy - fz)

		return torch.stack([lum, lab_a, lab_b], -1)

	@classmethod
	def _spectrum(cls, eigval: torch.Tensor, eigvec: torch.Tensor, transform: Callable[[torch.Tensor], torch.Tensor]) -> torch.Tensor:
		return eigvec @ torch.diag_embed(transform(eigval)) @ eigvec.transpose(1, 2)

	@classmethod
	def _square_root(cls, covariance: torch.Tensor) -> torch.Tensor:
		eigval, eigvec = cls._eigendecomposition(covariance)
		return cls._spectrum(eigval, eigvec, lambda eigval: eigval.clamp_min(0).sqrt())

	@classmethod
	def _standard_deviation(cls, tensor: torch.Tensor) -> torch.Tensor:
		return tensor.std(1, False)

	@classmethod
	def _wct(cls, features_i: torch.Tensor, features_r: torch.Tensor) -> torch.Tensor:
		if 2 > features_i.shape[1]:
			return features_i

		i_mean = cls._mean(features_i)
		r_mean = cls._mean(features_r)
		i_centered = features_i - i_mean.unsqueeze(1)
		r_centered = features_r - r_mean.unsqueeze(1)
		i_white = cls._inverse_square_root(cls._covariance(i_centered))
		r_color = cls._square_root(cls._covariance(r_centered))
		transform = r_color @ i_white
		return i_centered @ transform.transpose(1, 2) + r_mean.unsqueeze(1)

	@classmethod
	@abstractmethod
	def _match(cls, image: ColorMatchAlgorithmProfile, reference: ColorMatchAlgorithmProfile, strength: float, mask: torch.Tensor | None) -> torch.Tensor:
		raise NotImplementedError

	@classmethod
	@abstractmethod
	def _profile(cls, tensor: torch.Tensor) -> ColorMatchAlgorithmProfile:
		raise NotImplementedError

class HistogramMatching(ColorMatchAlgorithm[torch.Tensor]):
	@classmethod
	def _match(cls, image: torch.Tensor, reference: torch.Tensor, strength: float, mask: torch.Tensor | None) -> torch.Tensor:
		ibatch, iheight, iwidth, ichannel = image.shape
		rbatch, rheight, rwidth, rchannel = reference.shape

		iflat = image.view(ibatch, iheight * iwidth, ichannel)
		rflat = reference.view(rbatch, rheight * rwidth, rchannel)

		icount = iflat.shape[1]
		rcount = rflat.shape[1]

		if 2 > icount or 2 > rcount:
			return cls._lab_to_rgb(image)

		_, iindex = iflat.sort(1)
		rsorted, _ = rflat.sort(1)

		position = torch.arange(icount, device = image.device)
		rposition = (position * (rcount - 1) + (icount - 1) // 2) // (icount - 1)

		rposition = rposition.view(1, -1, 1).expand(rbatch, icount, rchannel)
		matched = rsorted.gather(1, rposition)

		result = torch.empty_like(iflat)
		result.scatter_(1, iindex, matched)
		result = result.view(ibatch, iheight, iwidth, ichannel)

		if mask is None:
			blended = strength * result + (1.0 - strength) * image
		else:
			weight = (strength * mask).unsqueeze(-1)
			blended = weight * result + (1.0 - weight) * image
		return cls._lab_to_rgb(blended)

	@classmethod
	def _profile(cls, tensor: torch.Tensor) -> torch.Tensor:
		return cls._rgb_to_lab(tensor)

class MGDMatching(ColorMatchAlgorithm[torch.Tensor]):
	@classmethod
	def _match(cls, image: torch.Tensor, reference: torch.Tensor, strength: float, mask: torch.Tensor | None) -> torch.Tensor:
		ibatch, iheight, iwidth, ichannel = image.shape
		rbatch, rheight, rwidth, rchannel = reference.shape

		iflat = image.view(ibatch, iheight * iwidth, ichannel)
		rflat = reference.view(rbatch, rheight * rwidth, rchannel)

		icount = iflat.shape[1]
		rcount = rflat.shape[1]

		if 2 > icount or 2 > rcount:
			return cls._lab_to_rgb(image)

		matched = cls._wct(iflat, rflat)
		result = matched.view(ibatch, iheight, iwidth, ichannel)
		if mask is None:
			blended = strength * result + (1.0 - strength) * image
		else:
			weight = (strength * mask).unsqueeze(-1)
			blended = weight * result + (1.0 - weight) * image
		return cls._lab_to_rgb(blended)

	@classmethod
	def _profile(cls, tensor: torch.Tensor) -> torch.Tensor:
		return cls._rgb_to_lab(tensor)

class MongeKantorovichLinear(ColorMatchAlgorithm[torch.Tensor]):
	@classmethod
	def _match(cls, image: torch.Tensor, reference: torch.Tensor, strength: float, mask: torch.Tensor | None) -> torch.Tensor:
		ibatch, iheight, iwidth, ichannel = image.shape
		rbatch, rheight, rwidth, rchannel = reference.shape

		iflat = image.view(ibatch, iheight * iwidth, ichannel)
		rflat = reference.view(rbatch, rheight * rwidth, rchannel)

		icount = iflat.shape[1]
		rcount = rflat.shape[1]

		if 2 > icount or 2 > rcount:
			return cls._lab_to_rgb(image)

		imean = cls._mean(iflat)
		rmean = cls._mean(rflat)

		icentered = iflat - imean.unsqueeze(1)
		rcentered = rflat - rmean.unsqueeze(1)

		icov = cls._covariance(icentered)
		rcov = cls._covariance(rcentered)

		ieigval, ieigvec = cls._eigendecomposition(icov)
		ihalf = cls._spectrum(ieigval, ieigvec, lambda eigval: eigval.clamp_min(0).sqrt())
		iinv = cls._spectrum(ieigval, ieigvec, lambda eigval: eigval.clamp_min(torch.finfo(eigval.dtype).eps).rsqrt())

		bhalf = cls._square_root(ihalf @ rcov @ ihalf)

		transform = iinv @ bhalf @ iinv
		matched = icentered @ transform + rmean.unsqueeze(1)

		result = matched.view(ibatch, iheight, iwidth, ichannel)
		if mask is None:
			blended = strength * result + (1.0 - strength) * image
		else:
			weight = (strength * mask).unsqueeze(-1)
			blended = weight * result + (1.0 - weight) * image
		return cls._lab_to_rgb(blended)

	@classmethod
	def _profile(cls, tensor: torch.Tensor) -> torch.Tensor:
		return cls._rgb_to_lab(tensor)

class ReinhardMatching(ColorMatchAlgorithm[torch.Tensor]):
	@classmethod
	def _match(cls, image: torch.Tensor, reference: torch.Tensor, strength: float, mask: torch.Tensor | None) -> torch.Tensor:
		ibatch, iheight, iwidth, ichannel = image.shape
		rbatch, rheight, rwidth, rchannel = reference.shape

		iflat = image.view(ibatch, iheight * iwidth, ichannel)
		rflat = reference.view(rbatch, rheight * rwidth, rchannel)

		icount = iflat.shape[1]
		rcount = rflat.shape[1]

		if 2 > icount or 2 > rcount:
			return cls._lab_to_rgb(image)

		imean = cls._mean(iflat)
		rmean = cls._mean(rflat)

		istd = cls._standard_deviation(iflat)
		rstd = cls._standard_deviation(rflat)

		istd.clamp_min_(torch.finfo(istd.dtype).eps)

		matched = (iflat - imean.unsqueeze(1)) * (rstd / istd).unsqueeze(1) + rmean.unsqueeze(1)

		result = matched.view(ibatch, iheight, iwidth, ichannel)
		if mask is None:
			blended = strength * result + (1.0 - strength) * image
		else:
			weight = (strength * mask).unsqueeze(-1)
			blended = weight * result + (1.0 - weight) * image
		return cls._lab_to_rgb(blended)

	@classmethod
	def _profile(cls, tensor: torch.Tensor) -> torch.Tensor:
		return cls._rgb_to_lab(tensor)

class WaveletMatching(ColorMatchAlgorithm[torch.Tensor]):
	LEVEL = 5

	G0A = [
		+0.0024118694566663, +0.0012775586538070, -0.0025761743066008, -0.0066287946124301,
		+0.0315263771220846, +0.0181564939455465, -0.1201885447107948, +0.0245501524336666,
		+0.5658080673964587, +0.7528160380878561, +0.2809028632221865, -0.1133058863621428,
		-0.0532761088030473, +0.0443652216066170, +0.0012834569993444, -0.0118347945154308,
		+0.0012098941630734, -0.0022841274402705,
	]

	G0B = [
		-0.0022841274402705, +0.0012098941630734, -0.0118347945154308, +0.0012834569993444,
		+0.0443652216066170, -0.0532761088030473, -0.1133058863621428, +0.2809028632221865,
		+0.7528160380878561, +0.5658080673964587, +0.0245501524336666, -0.1201885447107948,
		+0.0181564939455465, +0.0315263771220846, -0.0066287946124301, -0.0025761743066008,
		+0.0012775586538070, +0.0024118694566663,
	]

	G1A = [
		+0.0022841274402705, +0.0012098941630734, +0.0118347945154308, +0.0012834569993444,
		-0.0443652216066170, -0.0532761088030473, +0.1133058863621428, +0.2809028632221865,
		-0.7528160380878561, +0.5658080673964587, -0.0245501524336666, -0.1201885447107948,
		-0.0181564939455465, +0.0315263771220846, +0.0066287946124301, -0.0025761743066008,
		-0.0012775586538070, +0.0024118694566663,
	]

	G1B = [
		+0.0024118694566663, -0.0012775586538070, -0.0025761743066008, +0.0066287946124301,
		+0.0315263771220846, -0.0181564939455465, -0.1201885447107948, -0.0245501524336666,
		+0.5658080673964587, -0.7528160380878561, +0.2809028632221865, +0.1133058863621428,
		-0.0532761088030473, -0.0443652216066170, +0.0012834569993444, +0.0118347945154308,
		+0.0012098941630734, +0.0022841274402705,
	]

	H0A = [
		-0.0022841274402705, +0.0012098941630734, -0.0118347945154308, +0.0012834569993444,
		+0.0443652216066170, -0.0532761088030473, -0.1133058863621428, +0.2809028632221865,
		+0.7528160380878561, +0.5658080673964587, +0.0245501524336666, -0.1201885447107948,
		+0.0181564939455465, +0.0315263771220846, -0.0066287946124301, -0.0025761743066008,
		+0.0012775586538070, +0.0024118694566663,
	]

	H0B = [
		+0.0024118694566663, +0.0012775586538070, -0.0025761743066008, -0.0066287946124301,
		+0.0315263771220846, +0.0181564939455465, -0.1201885447107948, +0.0245501524336666,
		+0.5658080673964587, +0.7528160380878561, +0.2809028632221865, -0.1133058863621428,
		-0.0532761088030473, +0.0443652216066170, +0.0012834569993444, -0.0118347945154308,
		+0.0012098941630734, -0.0022841274402705,
	]

	H1A = [
		+0.0024118694566663, -0.0012775586538070, -0.0025761743066008, +0.0066287946124301,
		+0.0315263771220846, -0.0181564939455465, -0.1201885447107948, -0.0245501524336666,
		+0.5658080673964587, -0.7528160380878561, +0.2809028632221865, +0.1133058863621428,
		-0.0532761088030473, -0.0443652216066170, +0.0012834569993444, +0.0118347945154308,
		+0.0012098941630734, +0.0022841274402705,
	]

	H1B = [
		+0.0022841274402705, +0.0012098941630734, +0.0118347945154308, +0.0012834569993444,
		-0.0443652216066170, -0.0532761088030473, +0.1133058863621428, +0.2809028632221865,
		-0.7528160380878561, +0.5658080673964587, -0.0245501524336666, -0.1201885447107948,
		-0.0181564939455465, +0.0315263771220846, +0.0066287946124301, -0.0025761743066008,
		-0.0012775586538070, +0.0024118694566663,
	]

	L1_G0O = [
		+0.0000706263950893, +0.0000000000000000, -0.0013419015066964, -0.0018833705357143,
		+0.0071568080357143, +0.0238560267857143, -0.0556431361607143, -0.0516880580357143,
		+0.2997576032366072, +0.5594308035714286, +0.2997576032366072, -0.0516880580357143,
		-0.0556431361607143, +0.0238560267857143, +0.0071568080357143, -0.0018833705357143,
		-0.0013419015066964, +0.0000000000000000, +0.0000706263950893,
	]

	L1_G1O = [
		-0.0017578125000000, -0.0000000000000000, +0.0222656250000000, +0.0468750000000000,
		-0.0482421875000000, -0.2968750000000000, +0.5554687500000000, -0.2968750000000000,
		-0.0482421875000000, +0.0468750000000000, +0.0222656250000000, -0.0000000000000000,
		-0.0017578125000000,
	]

	L1_H0O = [
		-0.0017578125000000, +0.0000000000000000, +0.0222656250000000, -0.0468750000000000,
		-0.0482421875000000, +0.2968750000000000, +0.5554687500000000, +0.2968750000000000,
		-0.0482421875000000, -0.0468750000000000, +0.0222656250000000, +0.0000000000000000,
		-0.0017578125000000,
	]

	L1_H1O = [
		-0.0000706263950893, +0.0000000000000000, +0.0013419015066964, -0.0018833705357143,
		-0.0071568080357143, +0.0238560267857143, +0.0556431361607143, -0.0516880580357143,
		-0.2997576032366072, +0.5594308035714286, -0.2997576032366072, -0.0516880580357143,
		+0.0556431361607143, +0.0238560267857143, -0.0071568080357143, -0.0018833705357143,
		+0.0013419015066964, +0.0000000000000000, -0.0000706263950893,
	]

	@classmethod
	def _c2q(cls, w1: tuple[torch.Tensor, torch.Tensor], w2: tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
		w1r, w1i = w1
		w2r, w2i = w2
		x1 = w1r + w2r
		x2 = w1i + w2i
		x3 = w1i - w2i
		x4 = -w1r + w2r
		channel = w1r.shape[0]
		height = w1r.shape[-2]
		width = w1r.shape[-1]
		y = torch.zeros(channel, 2 * height, 2 * width, dtype = w1r.dtype, device = w1r.device)
		y[..., 0::2, 0::2] = x1
		y[..., 0::2, 1::2] = x2
		y[..., 1::2, 0::2] = x3
		y[..., 1::2, 1::2] = x4
		return y / math.sqrt(2.0)

	@classmethod
	def _analysis_higher(cls, x: torch.Tensor) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
		lo = cls._row_dual_filter_low(x, cls.H0B, cls.H0A)
		hi = cls._row_dual_filter_high(x, cls.H1B, cls.H1A)
		ll = cls._col_dual_filter_low(lo, cls.H0B, cls.H0A)
		lh = cls._col_dual_filter_high(lo, cls.H1B, cls.H1A)
		hl = cls._col_dual_filter_low(hi, cls.H0B, cls.H0A)
		hh = cls._col_dual_filter_high(hi, cls.H1B, cls.H1A)
		return ll, cls._highs_to_orientations(lh, hl, hh)

	@classmethod
	def _analysis_level_one(cls, x: torch.Tensor) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
		lo = cls._row_filter(x, cls.L1_H0O)
		hi = cls._row_filter(x, cls.L1_H1O)
		ll = cls._col_filter(lo, cls.L1_H0O)
		lh = cls._col_filter(lo, cls.L1_H1O)
		hl = cls._col_filter(hi, cls.L1_H0O)
		hh = cls._col_filter(hi, cls.L1_H1O)
		return ll, cls._highs_to_orientations(lh, hl, hh)

	@classmethod
	def _col_dual_filter_high(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_filter_1d(x, ha, hb, True, -2)

	@classmethod
	def _col_dual_filter_low(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_filter_1d(x, ha, hb, False, -2)

	@classmethod
	def _col_filter(cls, x: torch.Tensor, h: list[float]) -> torch.Tensor:
		return cls._filter_1d(x, h, -2)

	@classmethod
	def _col_inverse_filter_high(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_inverse_1d(x, ha, hb, True, -2)

	@classmethod
	def _col_inverse_filter_low(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_inverse_1d(x, ha, hb, False, -2)

	@classmethod
	def _decompose(cls, image: torch.Tensor, levels: int) -> list[tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]]:
		current = image.permute(2, 0, 1).contiguous()
		records: list[tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]] = []
		ll, complex_subbands = cls._analysis_level_one(current)
		records.append((ll, complex_subbands))
		current = ll
		for _ in range(2, levels + 1):
			ll, complex_subbands = cls._analysis_higher(current)
			records.append((ll, complex_subbands))
			current = ll
		return records

	@classmethod
	def _dual_filter_1d(cls, tensor: torch.Tensor, ha: list[float], hb: list[float], highpass: bool, dim: int) -> torch.Tensor:
		channel = tensor.shape[0]
		length = len(ha)
		size = tensor.shape[dim]
		positions = torch.arange(-length, size + length, device = tensor.device)
		modulo = positions % (2 * size)
		index = torch.where(modulo < size, modulo, 2 * size - modulo - 1)
		index_even = index[2::2]
		index_odd = index[3::2]
		x_even = tensor.index_select(dim, index_even)
		x_odd = tensor.index_select(dim, index_odd)
		x_cat = torch.cat([x_even, x_odd])
		wa = torch.tensor(ha, dtype = tensor.dtype, device = tensor.device)
		wb = torch.tensor(hb, dtype = tensor.dtype, device = tensor.device)
		match dim:
			case -2:
				wa_4d = wa.view(1, 1, length, 1).expand(channel, 1, length, 1)
				wb_4d = wb.view(1, 1, length, 1).expand(channel, 1, length, 1)
				weight = torch.cat([wa_4d, wb_4d], 0)
				stride = (2, 1)
			case _:
				wa_4d = wa.view(1, 1, 1, length).expand(channel, 1, 1, length)
				wb_4d = wb.view(1, 1, 1, length).expand(channel, 1, 1, length)
				weight = torch.cat([wa_4d, wb_4d], 0)
				stride = (1, 2)
		out = torch.nn.functional.conv2d(x_cat.unsqueeze(0), weight, stride = stride, groups = 2 * channel).squeeze(0)
		out_a = out[:channel]
		out_b = out[channel:]
		match highpass:
			case True:
				first, second = out_b, out_a
			case _:
				first, second = out_a, out_b
		match dim:
			case -2:
				stacked = torch.stack([first, second], 2)
				return stacked.reshape(channel, -1, tensor.shape[-1])
			case _:
				stacked = torch.stack([first, second], 3)
				return stacked.reshape(channel, tensor.shape[-2], -1)

	@classmethod
	def _dual_inverse_1d(cls, tensor: torch.Tensor, ha: list[float], hb: list[float], highpass: bool, dim: int) -> torch.Tensor:
		channel = tensor.shape[0]
		length = len(ha)
		half = length // 2
		size_half = tensor.shape[dim]
		ha_even = ha[0::2]
		ha_odd = ha[1::2]
		hb_even = hb[0::2]
		hb_odd = hb[1::2]
		positions = torch.arange(-half, size_half + half, device = tensor.device)
		modulo = positions % (2 * size_half)
		index = torch.where(modulo < size_half, modulo, 2 * size_half - modulo - 1)
		match half % 2:
			case 0:
				match highpass:
					case True:
						i1, i2, i3, i4 = index[1:-2:2], index[:-2:2], index[3::2], index[2::2]
					case _:
						i1, i2, i3, i4 = index[:-2:2], index[1:-2:2], index[2::2], index[3::2]
				h1, h2, h3, h4 = ha_even, hb_even, ha_odd, hb_odd
			case _:
				match highpass:
					case True:
						i1, i2, i3, i4 = index[2:-1:2], index[1:-1:2], index[2:-1:2], index[1:-1:2]
					case _:
						i1, i2, i3, i4 = index[1:-1:2], index[2:-1:2], index[1:-1:2], index[2:-1:2]
				h1, h2, h3, h4 = ha_odd, hb_odd, ha_even, hb_even
		x1 = tensor.index_select(dim, i1)
		x2 = tensor.index_select(dim, i2)
		x3 = tensor.index_select(dim, i3)
		x4 = tensor.index_select(dim, i4)
		x_cat = torch.cat([x1, x2, x3, x4], 0)
		kernel = len(h1)
		w1 = torch.tensor(h1, dtype = tensor.dtype, device = tensor.device)
		w2 = torch.tensor(h2, dtype = tensor.dtype, device = tensor.device)
		w3 = torch.tensor(h3, dtype = tensor.dtype, device = tensor.device)
		w4 = torch.tensor(h4, dtype = tensor.dtype, device = tensor.device)
		match dim:
			case -2:
				w1_4d = w1.view(1, 1, kernel, 1).expand(channel, 1, kernel, 1)
				w2_4d = w2.view(1, 1, kernel, 1).expand(channel, 1, kernel, 1)
				w3_4d = w3.view(1, 1, kernel, 1).expand(channel, 1, kernel, 1)
				w4_4d = w4.view(1, 1, kernel, 1).expand(channel, 1, kernel, 1)
			case _:
				w1_4d = w1.view(1, 1, 1, kernel).expand(channel, 1, 1, kernel)
				w2_4d = w2.view(1, 1, 1, kernel).expand(channel, 1, 1, kernel)
				w3_4d = w3.view(1, 1, 1, kernel).expand(channel, 1, 1, kernel)
				w4_4d = w4.view(1, 1, 1, kernel).expand(channel, 1, 1, kernel)
		weight = torch.cat([w1_4d, w2_4d, w3_4d, w4_4d], 0)
		out = torch.nn.functional.conv2d(x_cat.unsqueeze(0), weight, groups = 4 * channel).squeeze(0)
		o1 = out[:channel]
		o2 = out[channel:2 * channel]
		o3 = out[2 * channel:3 * channel]
		o4 = out[3 * channel:]
		match dim:
			case -2:
				stacked = torch.stack([o1, o2, o3, o4], 2)
				return stacked.reshape(channel, -1, tensor.shape[-1])
			case _:
				stacked = torch.stack([o1, o2, o3, o4], 3)
				return stacked.reshape(channel, tensor.shape[-2], -1)

	@classmethod
	def _filter_1d(cls, tensor: torch.Tensor, kernel: list[float], dim: int) -> torch.Tensor:
		length = len(kernel)
		radius = length // 2
		left = radius
		right = length - 1 - radius
		padded = cls._symmetric_pad(tensor, left, right, dim)
		weight = torch.tensor(kernel, dtype = tensor.dtype, device = tensor.device)
		padded_4d = padded.unsqueeze(1)
		match dim:
			case -2:
				weight_4d = weight.view(1, 1, length, 1)
				return torch.nn.functional.conv2d(padded_4d, weight_4d).squeeze(1)
			case _:
				weight_4d = weight.view(1, 1, 1, length)
				return torch.nn.functional.conv2d(padded_4d, weight_4d).squeeze(1)

	@classmethod
	def _highs_to_orientations(cls, lh: torch.Tensor, hl: torch.Tensor, hh: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
		(deg15r, deg15i), (deg165r, deg165i) = cls._q2c(lh)
		(deg45r, deg45i), (deg135r, deg135i) = cls._q2c(hh)
		(deg75r, deg75i), (deg105r, deg105i) = cls._q2c(hl)
		reals = torch.stack([deg15r, deg45r, deg75r, deg105r, deg135r, deg165r], 0)
		imags = torch.stack([deg15i, deg45i, deg75i, deg105i, deg135i, deg165i], 0)
		return reals, imags

	@classmethod
	def _match(cls, image: torch.Tensor, reference: torch.Tensor, strength: float, mask: torch.Tensor | None) -> torch.Tensor:
		i_mean = image.mean((1, 2), True)
		r_mean = reference.mean((1, 2), True)
		shifted = image - i_mean + r_mean
		ibatch, iheight, iwidth, _ = shifted.shape
		rbatch, rheight, rwidth, _ = reference.shape
		match min(iheight, iwidth, rheight, rwidth):
			case 0 | 1:
				return cls._lab_to_rgb(image)
			case _:
				results: list[torch.Tensor] = []
				for index in range(ibatch):
					results.append(cls._match_single(shifted[index], reference[index % rbatch]))
				matched = torch.stack(results, 0)
				if mask is None:
					blended = strength * matched + (1.0 - strength) * image
				else:
					weight = (strength * mask).unsqueeze(-1)
					blended = weight * matched + (1.0 - weight) * image
				return cls._lab_to_rgb(blended)

	@classmethod
	def _match_ll(cls, image_ll: torch.Tensor, reference_ll: torch.Tensor) -> torch.Tensor:
		channel, _, _ = image_ll.shape
		i_l_mean = image_ll[0].mean()
		r_l_mean = reference_ll[0].mean()
		matched_l = image_ll[:1] - i_l_mean + r_l_mean
		return torch.cat([matched_l, image_ll[1:channel]], 0)

	@classmethod
	def _match_orientations(cls, i_complex: tuple[torch.Tensor, torch.Tensor], r_complex: tuple[torch.Tensor, torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor]:
		i_reals, i_imags = i_complex
		r_reals, r_imags = r_complex
		orientations = i_reals.shape[0]
		channel = i_reals.shape[1]
		i_height = i_reals.shape[2]
		i_width = i_reals.shape[3]
		r_height = r_reals.shape[2]
		r_width = r_reals.shape[3]
		i_real_feat = i_reals.reshape(orientations, channel, i_height * i_width).transpose(1, 2)
		r_real_feat = r_reals.reshape(orientations, channel, r_height * r_width).transpose(1, 2)
		i_imag_feat = i_imags.reshape(orientations, channel, i_height * i_width).transpose(1, 2)
		r_imag_feat = r_imags.reshape(orientations, channel, r_height * r_width).transpose(1, 2)
		matched_real = cls._wct(i_real_feat, r_real_feat)
		matched_imag = cls._wct(i_imag_feat, r_imag_feat)
		matched_real = matched_real.transpose(1, 2).reshape(orientations, channel, i_height, i_width)
		matched_imag = matched_imag.transpose(1, 2).reshape(orientations, channel, i_height, i_width)
		return matched_real, matched_imag

	@classmethod
	def _match_single(cls, image: torch.Tensor, reference: torch.Tensor) -> torch.Tensor:
		height, width, _ = image.shape
		multiple = 2 ** cls.LEVEL
		pad_h = (-height) % multiple
		pad_w = (-width) % multiple
		if 0 < pad_h or 0 < pad_w:
			image = torch.nn.functional.pad(image.unsqueeze(0), (0, 0, 0, pad_w, 0, pad_h), "replicate").squeeze(0)
		r_height, r_width, _ = reference.shape
		r_pad_h = (-r_height) % multiple
		r_pad_w = (-r_width) % multiple
		if 0 < r_pad_h or 0 < r_pad_w:
			reference = torch.nn.functional.pad(reference.unsqueeze(0), (0, 0, 0, r_pad_w, 0, r_pad_h), "replicate").squeeze(0)
		work_height, work_width = image.shape[:2]
		i_records = cls._decompose(image, cls.LEVEL)
		r_records = cls._decompose(reference, cls.LEVEL)
		for j in range(cls.LEVEL):
			i_ll, i_complex = i_records[j]
			r_ll, r_complex = r_records[j]
			i_records[j] = (cls._match_ll(i_ll, r_ll), i_complex)
		for j in range(cls.LEVEL):
			i_ll, i_complex = i_records[j]
			r_ll, r_complex = r_records[j]
			i_records[j] = (i_ll, cls._match_orientations(i_complex, r_complex))
		result = cls._reconstruct(i_records, cls.LEVEL, work_height, work_width)
		result = result[:height, :width]
		return result

	@classmethod
	def _orientations_to_highs(cls, complex_subbands: tuple[torch.Tensor, torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
		reals, imags = complex_subbands
		lh = cls._c2q((reals[0], imags[0]), (reals[5], imags[5]))
		hh = cls._c2q((reals[1], imags[1]), (reals[4], imags[4]))
		hl = cls._c2q((reals[2], imags[2]), (reals[3], imags[3]))
		return lh, hl, hh

	@classmethod
	def _profile(cls, tensor: torch.Tensor) -> torch.Tensor:
		return cls._rgb_to_lab(tensor)

	@classmethod
	def _q2c(cls, y: torch.Tensor) -> tuple[tuple[torch.Tensor, torch.Tensor], tuple[torch.Tensor, torch.Tensor]]:
		s = math.sqrt(2.0)
		a = y[..., 0::2, 0::2] / s
		b = y[..., 0::2, 1::2] / s
		c = y[..., 1::2, 0::2] / s
		d = y[..., 1::2, 1::2] / s
		return (a - d, b + c), (a + d, b - c)

	@classmethod
	def _reconstruct(cls, records: list[tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]], levels: int, original_h: int, original_w: int) -> torch.Tensor:
		ll = records[levels - 1][0]
		for j in range(levels, 0, -1):
			_, complex_subbands = records[j - 1]
			match j:
				case 1:
					ll = cls._synthesis_level_one(ll, complex_subbands)
				case _:
					ll = cls._synthesis_higher(ll, complex_subbands)
		ll = ll[:, :original_h, :original_w]
		return ll.permute(1, 2, 0)

	@classmethod
	def _row_dual_filter_high(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_filter_1d(x, ha, hb, True, -1)

	@classmethod
	def _row_dual_filter_low(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_filter_1d(x, ha, hb, False, -1)

	@classmethod
	def _row_filter(cls, x: torch.Tensor, h: list[float]) -> torch.Tensor:
		return cls._filter_1d(x, h, -1)

	@classmethod
	def _row_inverse_filter_high(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_inverse_1d(x, ha, hb, True, -1)

	@classmethod
	def _row_inverse_filter_low(cls, x: torch.Tensor, ha: list[float], hb: list[float]) -> torch.Tensor:
		return cls._dual_inverse_1d(x, ha, hb, False, -1)

	@classmethod
	def _symmetric_pad(cls, tensor: torch.Tensor, left: int, right: int, dim: int) -> torch.Tensor:
		match (left, right):
			case (0, 0):
				return tensor
			case _:
				size = tensor.shape[dim]
				m = max(left, right)
				positions = torch.arange(-m, size + m, device = tensor.device)
				indices = positions % (2 * size)
				indices = torch.where(
					indices < size,
					indices,
					2 * size - indices - 1,
				)
				indices = indices[m - left : m - left + size + left + right]
				return tensor.index_select(dim, indices)

	@classmethod
	def _synthesis_higher(cls, ll: torch.Tensor, complex_subbands: tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
		lh, hl, hh = cls._orientations_to_highs(complex_subbands)
		hi = cls._col_inverse_filter_high(hh, cls.G1B, cls.G1A) + cls._col_inverse_filter_low(hl, cls.G0B, cls.G0A)
		lo = cls._col_inverse_filter_high(lh, cls.G1B, cls.G1A) + cls._col_inverse_filter_low(ll, cls.G0B, cls.G0A)
		return cls._row_inverse_filter_high(hi, cls.G1B, cls.G1A) + cls._row_inverse_filter_low(lo, cls.G0B, cls.G0A)

	@classmethod
	def _synthesis_level_one(cls, ll: torch.Tensor, complex_subbands: tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
		lh, hl, hh = cls._orientations_to_highs(complex_subbands)
		hi = cls._col_filter(hh, cls.L1_G1O) + cls._col_filter(hl, cls.L1_G0O)
		lo = cls._col_filter(lh, cls.L1_G1O) + cls._col_filter(ll, cls.L1_G0O)
		return cls._row_filter(hi, cls.L1_G1O) + cls._row_filter(lo, cls.L1_G0O)

class WhiteningColoringTransform(MongeKantorovichLinear):
	@classmethod
	def _match(cls, image: torch.Tensor, reference: torch.Tensor, strength: float, mask: torch.Tensor | None) -> torch.Tensor:
		ibatch, iheight, iwidth, ichannel = image.shape
		rbatch, rheight, rwidth, rchannel = reference.shape

		iflat = image.view(ibatch, iheight * iwidth, ichannel)
		rflat = reference.view(rbatch, rheight * rwidth, rchannel)

		icount = iflat.shape[1]
		rcount = rflat.shape[1]

		if 2 > icount or 2 > rcount:
			return cls._lab_to_rgb(image)

		matched = cls._wct(iflat, rflat)
		result = matched.view(ibatch, iheight, iwidth, ichannel)
		if mask is None:
			blended = strength * result + (1.0 - strength) * image
		else:
			weight = (strength * mask).unsqueeze(-1)
			blended = weight * result + (1.0 - weight) * image
		return cls._lab_to_rgb(blended)
