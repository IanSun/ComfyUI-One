import type { BaseUIComponentProps } from "@base-ui/react/internals/types";
import type { ComponentProps, FunctionComponent, KeyboardEvent, MouseEvent, PointerEvent, TouchEvent } from "react";

import { mergeProps, NumberField as NumberFieldPrimitive } from "@base-ui/react";
import { createGenericEventDetails } from "@base-ui/react/internals/createBaseUIEventDetails";
import { REASONS } from "@base-ui/react/internals/reasons";
import { useRenderElement } from "@base-ui/react/internals/useRenderElement";
import { useNumberFieldRootContext } from "@base-ui/react/number-field/root/NumberFieldRootContext";
import { NumberFieldScrubAreaContext } from "@base-ui/react/number-field/scrub-area/NumberFieldScrubAreaContext";
import { stateAttributesMapping } from "@base-ui/react/number-field/utils/stateAttributesMapping";
import { useDrag } from "@use-gesture/react";
import { memo, useEffect, useMemo, useRef, useState } from "react";
import { Field } from "./field";

export const NumberField = memo(({
	className,
	smallStep,
	step,
	...props
}: Omit<NumberFieldPrimitive.Root.Props, "className"> & Pick<ComponentProps<typeof Field>, "className">) => {
	const props_ref = useRef<Omit<NumberFieldPrimitive.Root.Props, "className">>({
		smallStep,
		step,
		...props,
	});

	({ smallStep, step } = useMemo(
		() => mergeProps<FunctionComponent<Pick<NumberFieldPrimitive.Root.Props, "smallStep" | "step">>>(
			{ smallStep: "number" === typeof step ? step : undefined },
			{ smallStep },
		),
		[smallStep, step],
	));

	props_ref.current = {
		smallStep,
		step,
		...props,
	};

	return <Field className={className}>
		<NumberFieldPrimitive.Root
			smallStep={smallStep}
			step={step}
			{...props}
		/>
	</Field>;
});

export const NumberFieldInput = memo(({
	className,
	...props
}: NumberFieldPrimitive.Input.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<NumberFieldPrimitive.Input.Props, "className">>>(
			{ className },
			{ className: "one:placeholder:text-muted-foreground" },
			{ className: "one:block one:h-8 one:w-full one:rounded-lg one:border-none one:bg-background one:py-0 one:px-2.5 one:text-sm one:text-current one:outline one:outline-solid one:-outline-offset-1 one:outline-input one:focus-visible:outline-ring one:ring-0 one:focus-visible:ring-3 one:ring-ring/0 one:focus-visible:ring-ring/50 one:outline-none one:disabled:opacity-50 one:transition-[box-shadow,opacity,outline-color] one:select-none one:cursor-auto" },
		),
		[className],
	));

	return <NumberFieldPrimitive.Input
		className={className}
		{...props}
	/>;
});

export const NumberFieldScrubArea = memo(({
	ref,
	...props
}: BaseUIComponentProps<"div", NumberFieldPrimitive.ScrubArea.State> & Omit<NumberFieldPrimitive.ScrubArea.Props, "teleportDistance" | keyof BaseUIComponentProps<"span", NumberFieldPrimitive.ScrubArea.State>>) => {
	const {
		className,
		direction = "horizontal",
		pixelSensitivity = 2,
		render,
		style,
		...element_props
	} = props;

	const {
		allowInputSyncRef,
		focusInput,
		getStepAmount,
		incrementValue,
		inputRef,
		lastChangedValueRef,
		onValueCommitted,
		setIsScrubbing: setRootScrubbing,
		state,
		valueRef,
	} = useNumberFieldRootContext();

	const { disabled, readOnly } = state;

	const scrub_area_ref = useRef<HTMLDivElement>(null);
	const scrub_area_cursor_ref = useRef<HTMLDivElement>(null);

	const [is_scrubbing, set_is_scrubbing] = useState(false);
	const [is_touch_input, set_is_touch_input] = useState(false);

	const context_value = useMemo(
		() => ({
			isPointerLockDenied: true,
			isScrubbing: is_scrubbing,
			isTouchInput: is_touch_input,
			scrubAreaCursorRef: scrub_area_cursor_ref,
		}),
		[is_scrubbing, is_touch_input],
	);

	const gesture_props = useDrag<KeyboardEvent<HTMLDivElement> | MouseEvent<HTMLDivElement> | PointerEvent<HTMLDivElement> | TouchEvent<HTMLDivElement>>(
		({ delta, event, first, last, tap }) => {
			if (!inputRef.current || tap) {
				return;
			}

			const { nativeEvent } = event;

			if (nativeEvent instanceof KeyboardEvent) {
				return;
			}

			if (first) {
				focusInput();
			}

			setRootScrubbing(!last);
			set_is_scrubbing(!last);
			set_is_touch_input(nativeEvent instanceof TouchEvent || nativeEvent instanceof PointerEvent && "touch" === nativeEvent.pointerType);

			const delta_value = Math.round("vertical" === direction ? -delta[1] : delta[0]);
			const step_amount = getStepAmount(event);
			const raw_amount = delta_value * step_amount;

			if (0 !== raw_amount) {
				allowInputSyncRef.current = true;
				incrementValue(
					Math.abs(raw_amount),
					{
						direction: 0 <= raw_amount ? 1 : -1,
						event,
						reason: REASONS.scrub,
					},
				);
			}

			if (last) {
				onValueCommitted(
					lastChangedValueRef.current ?? valueRef.current,
					createGenericEventDetails(REASONS.scrub, nativeEvent as globalThis.PointerEvent),
				);
			}
		},
		{
			axis: "x",
			axisThreshold: {
				mouse: pixelSensitivity,
				pen: pixelSensitivity,
				touch: pixelSensitivity,
			},
			filterTaps: true,
			preventDefault: true,
		},
	)();

	const default_props: ComponentProps<"div"> = {
		className: "one:h-3 one:w-7.5 one:bg-[radial-gradient(currentColor_1px,transparent_1px)] one:bg-size-[4px_4px] one:bg-center one:text-muted one:select-none one:touch-none one:cursor-ew-resize",
		role: "presentation",
	};

	const element = useRenderElement(
		"div",
		props,
		{
			props: [default_props, ...disabled || readOnly ? [] : [gesture_props], element_props],
			ref: [ref, scrub_area_ref],
			state,
			stateAttributesMapping,
		},
	);

	useEffect(
		() => {
			return () => {
				setRootScrubbing(false);
			};
		},
		[setRootScrubbing],
	);

	return <NumberFieldScrubAreaContext value={context_value}>
		{element}
	</NumberFieldScrubAreaContext>;
});
