import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { mergeProps } from "react-aria";
import {
	Button as ButtonPrimitive,
	ColorArea as ColorAreaPrimitive,
	ColorPicker as ColorPickerPrimitive,
	ColorSlider as ColorSliderPrimitive,
	ColorSwatchPickerItem as ColorSwatchPickerItemPrimitive,
	ColorSwatchPicker as ColorSwatchPickerPrimitive,
	ColorSwatch as ColorSwatchPrimitive,
	ColorThumb as ColorThumbPrimitive,
	composeRenderProps,
	DialogTrigger as DialogTriggerPrimitive,
	Group as GroupPrimitive,
	SliderTrack as SliderTrackPrimitive,
} from "react-aria-components";
import { useMouseEventListeners, usePointerEventListeners, useTouchEventListeners } from "./hooks/interaction";
import { Popover } from "./popover";

export const ColorArea = memo(({
	className,
	...props
}: ComponentProps<typeof ColorAreaPrimitive>) => {
	props = mergeProps(
		props,
		useMouseEventListeners(),
		usePointerEventListeners(),
		useTouchEventListeners(),
	);

	return <ColorAreaPrimitive
		className={cn(
			"w-full aspect-3/2 rounded-md bg-component-node-widget-background select-none cursor-auto",
			className,
		)}
		data-slot="color-area"
		{...props}
	>
		<ColorThumb data-slot="color-area-thumb" />
	</ColorAreaPrimitive>;
});

export const ColorPicker = memo((
	{
		children,
		className,
		...props
	}:
		& Omit<ComponentProps<typeof ColorPickerPrimitive>, "children">
		& Pick<ComponentProps<typeof DialogTriggerPrimitive>, "children">
		& Pick<ComponentProps<typeof GroupPrimitive>, "className">,
) => {
	return <ColorPickerPrimitive {...props}>
		<DialogTriggerPrimitive>
			<GroupPrimitive
				children={children}
				className={cn(
					"relative flex items-center justify-center select-none cursor-auto",
					className,
				)}
				data-slot="color-picker"
			/>
		</DialogTriggerPrimitive>
	</ColorPickerPrimitive>;
});

export const ColorPickerContent = memo(({
	className,
	containerPadding = 0,
	offset = 6,
	...props
}: ComponentProps<typeof Popover>) => {
	return <Popover
		className={cn(
			"flex w-64 rounded-lg py-2.5 px-3 flex-col gap-2",
			className,
		)}
		containerPadding={containerPadding}
		data-slot="color-picker-content"
		offset={offset}
		{...props}
	/>;
});

export const ColorPickerSwatch = memo(({
	className,
	...props
}: ComponentProps<typeof ButtonPrimitive>) => {
	return <ButtonPrimitive
		className={cn(
			"shrink-0 rounded-full border-none bg-transparent p-0 overflow-hidden outline-none ring-0 ring-component-node-widget-background/0 shadow-none focus:ring focus:ring-component-node-widget-background-hovered focus:shadow-sm pressed:ring pressed:ring-component-node-widget-background-selected pressed:shadow-sm transition-[background-color,box-shadow] select-none cursor-auto",
			className,
		)}
		data-slot="color-picker-swatch"
		{...props}
	>
		<ColorSwatch />
	</ButtonPrimitive>;
});

export const ColorSlider = memo(({
	className,
	...props
}: ComponentProps<typeof ColorSliderPrimitive>) => {
	return <ColorSliderPrimitive
		className={cn(
			"relative h-2.5 w-full rounded-full bg-component-node-widget-background select-none cursor-auto",
			className,
		)}
		data-slot="color-slider"
		{...props}
	>
		<SliderTrack data-slot="color-slider-track" />
		<ColorThumb data-slot="color-slider-thumb" />
	</ColorSliderPrimitive>;
});

export const ColorSwatch = memo(({
	className,
	style,
	...props
}: ComponentProps<typeof ColorSwatchPrimitive>) => {
	return <div className="shrink-0 flex size-6 rounded-full items-center justify-center overflow-hidden select-none cursor-auto">
		<ColorSwatchPrimitive
			className={cn(
				"shrink-0 size-5.5 rounded-full",
				className,
			)}
			data-slot="color-swatch"
			style={composeRenderProps(style, (style, { color }) => ({
				...style,
				backgroundColor: "#000",
				backgroundImage: `linear-gradient(${color.toString("css")}), repeating-conic-gradient(rgba(255, 255, 255, 0.5) 0% 25%, rgba(255, 255, 255, 0.3) 25% 50%)`,
			}))}
			{...props}
		/>
	</div>;
});

export const ColorSwatchPicker = memo(({
	className,
	...props
}: ComponentProps<typeof ColorSwatchPickerPrimitive>) => {
	return <ColorSwatchPickerPrimitive
		className={cn(
			"grid grid-cols-[repeat(auto-fill,1.5rem)] justify-between gap-1",
			className,
		)}
		{...props}
	/>;
});

export const ColorSwatchPickerItem = memo(({
	className,
	...props
}: ComponentProps<typeof ColorSwatchPickerItemPrimitive>) => {
	return <ColorSwatchPickerItemPrimitive
		className={cn(
			"shrink-0 rounded-full ring-0 ring-component-node-widget-background/0 selected:ring selected:ring-primary-background",
			className,
		)}
		{...props}
	/>;
});

const ColorThumb = memo(({
	className,
	...props
}: ComponentProps<typeof ColorThumbPrimitive>) => {
	props = mergeProps(
		props,
		useMouseEventListeners(),
		usePointerEventListeners(),
		useTouchEventListeners(),
	);

	return <ColorThumbPrimitive
		className={cn(
			"absolute top-[50%] size-3 rounded-full border border-component-node-foreground shadow-sm",
			className,
		)}
		data-slot="color-thumb"
		{...props}
	/>;
});

const SliderTrack = memo(({
	className,
	...props
}: ComponentProps<typeof SliderTrackPrimitive>) => {
	props = mergeProps(
		props,
		useMouseEventListeners(),
		usePointerEventListeners(),
		useTouchEventListeners(),
	);

	return <div className="h-full rounded-full bg-[repeating-conic-gradient(rgba(255,255,255,0.2)_0%_25%,rgba(255,255,255,0.1)_25%_50%)] bg-size-[10px,10px] pointer-events-none">
		<SliderTrackPrimitive
			className={cn(
				"h-full rounded-full pointer-events-auto",
				className,
			)}
			data-slot="slider-track"
			{...props}
		/>
	</div>;
});
