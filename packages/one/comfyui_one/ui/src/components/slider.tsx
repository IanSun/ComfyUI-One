import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { mergeProps } from "react-aria";
import {
	SliderFill as SliderFillPrimitive,
	Slider as SliderPrimitive,
	SliderThumb as SliderThumbPrimitive,
	SliderTrack as SliderTrackPrimitive,
} from "react-aria-components";
import { useMouseEventListeners, usePointerEventListeners, useTouchEventListeners } from "./hooks/interaction";

export const Slider = memo(({
	className,
	...props
}: ComponentProps<typeof SliderPrimitive>) => {
	return <SliderPrimitive
		className={cn(
			"group relative select-none cursor-auto touch-none",
			className,
		)}
		data-slot="slider"
		{...props}
	>
		{({ state }) => {
			return <>
				<SliderTrack>
					<SliderFillPrimitive
						className="absolute size-full rounded-full bg-primary-background pointer-events-none"
						data-slot="slider-range"
					/>
				</SliderTrack>
				{state.values.map((_, index) =>
					<SliderThumb
						index={index}
						key={index}
					/>)}
			</>;
		}}
	</SliderPrimitive>;
}) as typeof SliderPrimitive;

export const SliderSkeleton = memo(({
	className,
	orientation = "horizontal",
}: Pick<ComponentProps<typeof Slider>, "className" | "orientation">) => {
	return <div
		className={cn(
			"group relative select-none cursor-auto",
			className,
		)}
		data-orientation={orientation}
		data-slot="slider"
	>
		<div
			className="relative orientation-horizontal:h-1 rounded-full bg-component-node-widget-background overflow-hidden"
			data-orientation={orientation}
			data-slot="slider-track"
		>
			<div
				className="absolute size-full w-1/3 bg-component-node-foreground/20"
				data-orientation={orientation}
				data-slot="slider-range"
			/>
		</div>
		<div
			className="absolute inset-s-1/3 group-orientation-horizontal:top-[50%] size-3 rounded-full bg-component-node-foreground -translate-1/2"
			data-slot="slider-thumb"
		/>
	</div>;
});

const SliderThumb = memo(({
	className,
	...props
}: ComponentProps<typeof SliderThumbPrimitive>) => {
	props = mergeProps(
		props,
		useMouseEventListeners(),
		usePointerEventListeners(),
		useTouchEventListeners(),
	);

	return <SliderThumbPrimitive
		className={cn(
			"absolute group-orientation-horizontal:top-[50%] size-3 rounded-full bg-component-node-foreground ring-0 ring-component-node-widget-background/0 shadow-sm hover:ring-3 hover:ring-component-node-foreground/10 focus:ring-component-node-foreground/10 transition-shadow",
			className,
		)}
		data-slot="slider-thumb"
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

	return <SliderTrackPrimitive
		className={cn(
			"relative orientation-horizontal:h-1 rounded-full bg-component-node-widget-background overflow-hidden",
			className,
		)}
		data-slot="slider-track"
		{...props}
	/>;
});
