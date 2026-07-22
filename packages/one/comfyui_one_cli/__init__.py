from argparse import (
	Action,
	ArgumentParser,
	Namespace,
	RawDescriptionHelpFormatter,
	_HelpAction, # pyright: ignore[reportPrivateUsage]
	_SubParsersAction, # pyright: ignore[reportPrivateUsage]
)
from os import symlink
from pathlib import Path
from shutil import rmtree
from sys import exit, stderr
from typing import Any

def install(args: Namespace) -> None:
	dst = _resolve_custom_nodes_one_root(args.path)
	src = _resolve_one_root()

	try:
		if dst.exists(follow_symlinks = False):
			if dst.is_symlink():
				dst.unlink()
			else:
				rmtree(dst)

		symlink(
			src = src,
			dst = dst,
			target_is_directory = True,
		)

		print(
			"🎉 Installation successful!",
			"💡 Please restart ComfyUI to apply changes.",
			sep = "\n",
		)
	except Exception as error:
		print(
			"error: Installation failed.",
			f"details: {error}",
			sep = "\n",
			file = stderr,
		)

		exit(1)

def main() -> None:
	class CapitalizedHelpFormatter(RawDescriptionHelpFormatter):
		def _format_action(self, action: Action) -> str:
			if isinstance(action, _SubParsersAction):
				parts: list[str] = []

				for subaction in action._get_subactions():
					parts.append(super()._format_action(subaction))

				return "".join(parts)

			return super()._format_action(action)

		def _format_usage(self, *args: Any, **kwargs: Any) -> str:
			return super()._format_usage(*args, **kwargs).replace("usage:", "Usage:", 1)

		def _get_help_string(self, action: Action) -> str | None:
			if isinstance(action, _HelpAction):
				return "Show this help message and exit"

			return super()._get_help_string(action)

		def start_section(self, heading: str | None) -> None:
			match heading:
				case "commands":
					heading = "Commands"

				case "options":
					heading = "Options"

				case _:
					pass

			return super().start_section(heading)

	parser = ArgumentParser(
		description = "ComfyUI-One Command-Line Interface",
		formatter_class = CapitalizedHelpFormatter,
	)

	subparsers = parser.add_subparsers(
		title = "commands",
		dest = "command",
		required = True,
	)

	install_parser = subparsers.add_parser(
		name = "install",
		help = "Install ComfyUI-One into ComfyUI",
		description = "Install ComfyUI-One into ComfyUI",
		formatter_class = CapitalizedHelpFormatter,
	)
	install_parser.add_argument(
		"-p",
		"--path",
		help = "Explicit path to the ComfyUI root directory",
		metavar = "PATH",
		dest = "path",
	)
	install_parser.set_defaults(apply = install)

	uninstall_parser = subparsers.add_parser(
		name = "uninstall",
		help = "Uninstall ComfyUI-One from ComfyUI",
		description = "Uninstall ComfyUI-One from ComfyUI",
		formatter_class = CapitalizedHelpFormatter,
	)
	uninstall_parser.add_argument(
		"-p",
		"--path",
		help = "Explicit path to the ComfyUI root directory",
		metavar="PATH",
		dest = "path",
	)
	uninstall_parser.set_defaults(apply = uninstall)

	args = parser.parse_args()
	args.apply(args)

def uninstall(args: Namespace) -> None:
	link = _resolve_custom_nodes_one_root(args.path)

	print("🗑️ Uninstalling node [comfyui-one]...")

	try:
		if link.exists(follow_symlinks = False):
			if link.is_symlink():
				link.unlink()
			else:
				rmtree(link)

			print("🎉 Uninstallation successful!")

		else:
			print("ℹ️ Comfyui-One is not currently installed.")

	except Exception as error:
		print(
			"error: Uninstallation failed.",
			f"details: {error}",
			sep = "\n",
			file = stderr,
		)

		exit(1)

def _resolve_custom_nodes_dir(path: Path | None = None) -> Path:
	root = _resolve_root(path)

	return root / "custom_nodes"

def _resolve_custom_nodes_one_root(path: Path | None = None) -> Path:
	root = _resolve_custom_nodes_dir(path)

	return root / "One"

def _resolve_one_root() -> Path:
	root = Path(__file__).parent.parent.resolve() / "comfyui_one"

	if not (root / "__init__.py").exists():
		print(
			"error: Core package path could not be located.",
			file = stderr,
		)

		exit(1)

	return root

def _resolve_root(path: Path | None = None) -> Path:
	if path:
		root = Path(path).resolve()
	else:
		root = Path.cwd()

	if not (root / "custom_nodes").exists():
		print(
			"error: ComfyUI root directory could not be automatically detected.",
			"hint: Please specify the root path explicitly using the '--path' or '-p' flag.",
			sep = "\n",
			file = stderr,
		)

		exit(1)

	return root

if __name__ == "__main__":
	main()
