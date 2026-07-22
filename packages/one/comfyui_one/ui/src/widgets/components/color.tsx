import type { DOMWidgetProps } from "../../internal/node";
import type { ColorInputSpec, InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef } from "@/schemas/nodeDefSchema";
import type { ComponentProps, ReactNode } from "react";
import type { Color as ColorType } from "react-aria-components";

import { cn } from "cn";
import { Pipette, X } from "lucide-react";
import { memo, Suspense, useCallback, useMemo } from "react";
import { mergeProps } from "react-aria";
import { InputContext, useSlottedContext } from "react-aria-components";
import { Button } from "../../components/button";
import {
	ColorArea,
	ColorPicker,
	ColorPickerContent,
	ColorPickerSwatch,
	ColorSlider,
	ColorSwatch,
	ColorSwatchPicker,
	ColorSwatchPickerItem,
} from "../../components/color";
import { ColorField, Field, FieldLabel, FieldLabelSkeleton, FieldSkeleton } from "../../components/field";
import { Group } from "../../components/group";
import { InputGroup, InputGroupAddon, InputGroupInput } from "../../components/input-group";
import { Separator } from "../../components/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../components/tabs";
import { useValueProps } from "../hooks/component";
import { useNodeInputTranslation } from "../hooks/i18n";

type ColorSpec = { options?: { format?: "hex" | "hexa" } } & ColorInputSpec;

export const Color = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<string, ColorSpec>) => {
	const { options: { format = "hexa" } = {} } = specification;

	const props = useValueProps({
		serialize: useCallback((value: ColorType) => value.toString(format), [format]),
		store,
		widget,
	});

	return <Suspense>
		<Field>
			<ColorFieldLabel
				definition={definition}
				specification={specification}
			/>
			<Group className="flex gap-2">
				<ColorPicker {...props}>
					<ColorPickerSwatch />
					<ColorPickerContent
						offset={12}
						placement="start"
					>
						<ColorArea
							className="bg-component-node-background"
							colorSpace="hsb"
							xChannel="saturation"
							yChannel="brightness"
						/>
						<ColorSlider
							channel="hue"
							className="bg-component-node-background"
							colorSpace="hsb"
						/>
						{
							"hexa" === format
								? <ColorSlider
									channel="alpha"
									className="bg-component-node-background"
									colorSpace="rgb"
								/>
								: null
						}
						{
							(() => {
								switch (format) {
									case "hex": {
										return <Tabs defaultSelectedKey="RGB">
											<TabsList className="flex w-full">
												<TabsTrigger id="RGB">RGB</TabsTrigger>
												<TabsTrigger id="HSL">HSL</TabsTrigger>
												<TabsTrigger id="HSB">HSB</TabsTrigger>
											</TabsList>
											<TabsContent
												className="grid grid-cols-3 gap-2"
												id="RGB"
											>
												<ColorFieldRGB />
											</TabsContent>
											<TabsContent
												className="grid grid-cols-3 gap-2"
												id="HSL"
											>
												<ColorFieldHSL />
											</TabsContent>
											<TabsContent
												className="grid grid-cols-3 gap-2"
												id="HSB"
											>
												<ColorFieldHSB />
											</TabsContent>
										</Tabs>;
									}

									case "hexa": {
										return <Tabs defaultSelectedKey="RGBA">
											<TabsList className="flex w-full">
												<TabsTrigger id="RGBA">RGBA</TabsTrigger>
												<TabsTrigger id="HSLA">HSLA</TabsTrigger>
												<TabsTrigger id="HSBA">HSBA</TabsTrigger>
											</TabsList>
											<TabsContent
												className="grid grid-cols-3 gap-2"
												id="RGBA"
											>
												<ColorFieldRGB />
												<ColorFieldHexA />
											</TabsContent>
											<TabsContent
												className="grid grid-cols-3 gap-2"
												id="HSLA"
											>
												<ColorFieldHSL />
												<ColorFieldHexA />
											</TabsContent>
											<TabsContent
												className="grid grid-cols-3 gap-2"
												id="HSBA"
											>
												<ColorFieldHSB />
												<ColorFieldHexA />
											</TabsContent>
										</Tabs>;
									}

									default: {
										return null;
									}
								}
							})()
						}
						<Separator />
						<ColorSwatchPicker>
							<ColorSwatchPickerItem color="#000">
								<ColorSwatch />
							</ColorSwatchPickerItem>
							<ColorSwatchPickerItem color="#FFF">
								<ColorSwatch />
							</ColorSwatchPickerItem>
							<ColorSwatchPickerItem color="#808080">
								<ColorSwatch />
							</ColorSwatchPickerItem>
							<ColorSwatchPickerItem color="#F00">
								<ColorSwatch />
							</ColorSwatchPickerItem>
							<ColorSwatchPickerItem color="#0F0">
								<ColorSwatch />
							</ColorSwatchPickerItem>
							<ColorSwatchPickerItem color="#00F">
								<ColorSwatch />
							</ColorSwatchPickerItem>
						</ColorSwatchPicker>
					</ColorPickerContent>
				</ColorPicker>
				{
					"hexa" === format
						? <Group className="flex-1 grid grid-cols-5 gap-2">
							<ColorField
								{...props}
								className="col-span-3"
								colorSpace="rgb"
							>
								<ColorFieldInput
									prefix="#"
									trimPrefix="#"
								/>
							</ColorField>
							<ColorField
								{...props}
								channel="alpha"
								className="col-span-2"
								colorSpace="rgb"
							>
								<ColorFieldInput
									prefix={<div className="size-3 rounded-sm border border-component-node-foreground-secondary bg-[repeating-conic-gradient(transparent_0%_25%,var(--component-node-foreground-secondary)_25%_50%)]" />}
									suffix="%"
									trimSuffix="%"
								/>
							</ColorField>
						</Group>
						: <ColorField
							{...props}
							className="flex-1"
							colorSpace="rgb"
						>
							<ColorFieldInput
								prefix="#"
								trimPrefix="#"
							/>
						</ColorField>
				}
			</Group>
		</Field>
	</Suspense>;
});

const ColorFieldHSB = memo(() => {
	return <Group className="col-span-3 grid grid-cols-subgrid gap-2">
		<ColorField
			channel="hue"
			colorSpace="hsb"
		>
			<ColorFieldInput
				prefix="H"
				suffix="°"
				trimSuffix="°"
			/>
		</ColorField>
		<ColorField
			channel="saturation"
			colorSpace="hsb"
		>
			<ColorFieldInput
				prefix="S"
				suffix="%"
				trimSuffix="%"
			/>
		</ColorField>
		<ColorField
			channel="brightness"
			colorSpace="hsb"
		>
			<ColorFieldInput
				prefix="L"
				suffix="%"
				trimSuffix="%"
			/>
		</ColorField>
	</Group>;
});

const ColorFieldHSL = memo(() => {
	return <Group className="col-span-3 grid grid-cols-subgrid gap-2">
		<ColorField
			channel="hue"
			colorSpace="hsl"
		>
			<ColorFieldInput
				prefix="H"
				suffix="°"
				trimSuffix="°"
			/>
		</ColorField>
		<ColorField
			channel="saturation"
			colorSpace="hsl"
		>
			<ColorFieldInput
				prefix="S"
				suffix="%"
				trimSuffix="%"
			/>
		</ColorField>
		<ColorField
			channel="lightness"
			colorSpace="hsl"
		>
			<ColorFieldInput
				prefix="L"
				suffix="%"
				trimSuffix="%"
			/>
		</ColorField>
	</Group>;
});

const ColorFieldHexA = memo(() => {
	return <Group className="col-span-3 grid grid-cols-subgrid gap-2">
		<ColorField
			className="col-span-2"
			colorSpace="rgb"
		>
			<ColorFieldInput
				prefix="#"
				trimPrefix="#"
			/>
		</ColorField>
		<ColorField
			channel="alpha"
			colorSpace="rgb"
		>
			<ColorFieldInput
				prefix="A"
				suffix="%"
				trimSuffix="%"
			/>
		</ColorField>
	</Group>;
});

const ColorFieldInput = memo(({
	prefix,
	suffix,
	trimPrefix,
	trimSuffix,
}: {
	prefix?: ReactNode;
	suffix?: ReactNode;
	trimPrefix?: string;
	trimSuffix?: string;
}) => {
	const context = useSlottedContext(InputContext);

	const input_context = useMemo(() => {
		const value = context?.value;

		if ("string" === typeof value) {
			const props: typeof context = { value };

			if ("string" === typeof trimPrefix && value.startsWith(trimPrefix)) {
				props.value = value.slice(1);
			}

			if ("string" === typeof trimSuffix && value.endsWith(trimSuffix)) {
				props.value = value.slice(0, -1);
			}

			if (value !== props.value) {
				return mergeProps(context, props);
			}
		}

		return context;
	}, [context, trimPrefix, trimSuffix]);

	return <InputContext value={input_context}>
		<InputGroup>
			<InputGroupInput className={suffix ? "text-end" : undefined} />
			{prefix ? <InputGroupAddon>{prefix}</InputGroupAddon> : null}
			{suffix ? <InputGroupAddon align="inline-end">{suffix}</InputGroupAddon> : null}
		</InputGroup>
	</InputContext>;
});

const ColorFieldLabel = memo(({
	className,
	definition,
	specification,
}: {
	definition: ComfyNodeDef;
	specification: InputSpec;
} & Pick<ComponentProps<typeof FieldLabel>, "className">) => {
	const t = useNodeInputTranslation(definition, specification);

	return <FieldLabel className={className}>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const ColorFieldRGB = memo(() => {
	return <Group className="col-span-3 grid grid-cols-subgrid gap-2">
		<ColorField
			channel="red"
			colorSpace="rgb"
		>
			<InputGroup>
				<InputGroupInput className="text-end" />
				<InputGroupAddon>{"R"}</InputGroupAddon>
			</InputGroup>
		</ColorField>
		<ColorField
			channel="green"
			colorSpace="rgb"
		>
			<InputGroup>
				<InputGroupInput className="text-end" />
				<InputGroupAddon>{"G"}</InputGroupAddon>
			</InputGroup>
		</ColorField>
		<ColorField
			channel="blue"
			colorSpace="rgb"
		>
			<InputGroup>
				<InputGroupInput className="text-end" />
				<InputGroupAddon>{"B"}</InputGroupAddon>
			</InputGroup>
		</ColorField>
	</Group>;
});

const ColorFieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof ColorFieldLabel>, "className">) => {
	return <FieldLabelSkeleton className={className} />;
});
