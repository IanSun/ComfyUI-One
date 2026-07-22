import type { ComponentProps, FunctionComponent, NamedExoticComponent } from "react";
import type { SliderProps as SliderPrimitiveProps } from "react-aria-components";

import { cn } from "cn";
import { memo, useEffect, useRef } from "react";
import {
	SliderFill as SliderFillPrimitive,
	Slider as SliderPrimitive,
	SliderThumb as SliderThumbPrimitive,
	SliderTrack as SliderTrackPrimitive,
} from "react-aria-components";

export const Slider = memo(({
	className,
	...props
}: SliderPrimitiveProps) => {
	const ref = useRef<HTMLDivElement>(null);

	useEffect(() => {
		const element = ref.current;
		if (!element) {
			return;
		}

		const event_set = new WeakSet<PointerEvent>();
		const pointer_id_set = new Set<number>();

		const { ownerDocument } = element;

		const pointercancel_listener = (event: PointerEvent) => {
			const { pointerId } = event;

			if (event_set.has(event) || !pointer_id_set.has(pointerId)) {
				return;
			}

			ownerDocument.removeEventListener("pointercancel", pointercancel_listener, { capture: true });
			ownerDocument.removeEventListener("pointermove", pointermove_listener, { capture: true });
			ownerDocument.removeEventListener("pointerup", pointerup_listener, { capture: true });

			const new_event = new PointerEvent(event.type, event);
			event_set.add(new_event);

			event.preventDefault();
			event.stopPropagation();
			pointer_id_set.delete(pointerId);
			ownerDocument.dispatchEvent(new_event);
		};

		const pointerdown_listener = (event: PointerEvent) => {
			const { target } = event;
			if (!(target && target instanceof Node && element.contains(target))) {
				return;
			}

			pointer_id_set.add(event.pointerId);

			ownerDocument.addEventListener("pointercancel", pointercancel_listener, { capture: true });
			ownerDocument.addEventListener("pointermove", pointermove_listener, { capture: true });
			ownerDocument.addEventListener("pointerup", pointerup_listener, { capture: true });
		};

		const pointermove_listener = (event: PointerEvent) => {
			if (event_set.has(event) || !pointer_id_set.has(event.pointerId)) {
				return;
			}

			const new_event = new PointerEvent(event.type, event);
			event_set.add(new_event);

			event.preventDefault();
			event.stopPropagation();
			ownerDocument.dispatchEvent(new_event);
		};

		const pointerup_listener = pointercancel_listener;

		ownerDocument.addEventListener("pointerdown", pointerdown_listener, { capture: true });

		return () => {
			ownerDocument.removeEventListener("pointercancel", pointercancel_listener, { capture: true });
			ownerDocument.removeEventListener("pointerdown", pointerdown_listener, { capture: true });
			ownerDocument.removeEventListener("pointermove", pointermove_listener, { capture: true });
			ownerDocument.removeEventListener("pointerup", pointerup_listener, { capture: true });
		};
	}, []);

	return <SliderPrimitive
		className={cn(
			"group relative select-none cursor-auto touch-none",
			className,
		)}
		data-slot="slider"
		ref={ref}
		{...props}
	>
		{({ state }) => {
			return <>
				<SliderTrackPrimitive
					className="relative orientation-horizontal:h-1 rounded-full bg-component-node-widget-background overflow-hidden"
					data-slot="slider-track"
				>
					<SliderFillPrimitive
						className="absolute size-full bg-primary-background"
						data-slot="slider-range"
					/>
				</SliderTrackPrimitive>
				{state.values.map((_, index) =>
					<SliderThumbPrimitive
						className="absolute group-orientation-horizontal:top-[50%] size-3 rounded-full bg-component-node-foreground ring-0 hover:ring-3 hover:ring-component-node-widget-background-highlighted/40 focus-visible:ring-3 focus-visible:ring-component-node-widget-background-highlighted/40 active:ring-3 active:ring-component-node-widget-background-highlighted/40 transition-shadow cursor-grab"
						data-slot="slider-thumb"
						index={index}
						key={index}
					/>)}
			</>;
		}}
	</SliderPrimitive>;
}) as (
	NamedExoticComponent<SliderPrimitiveProps>
	& (<T extends number | number[]>(
		this: ThisParameterType<FunctionComponent<SliderPrimitiveProps<T>>>,
		...args: Parameters<FunctionComponent<SliderPrimitiveProps<T>>>
	) => ReturnType<FunctionComponent<SliderPrimitiveProps<T>>>)
);

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
