import type { Placement } from "@floating-ui/dom";
import type { ComponentProps, CSSProperties } from "react";

import {
	computePosition,
	arrow as floating_arrow,
	flip as floating_flip,
	offset as floating_float,
} from "@floating-ui/dom";
import { cn } from "cn";
import { memo, use, useCallback, useLayoutEffect, useMemo, useState } from "react";
import { mergeProps, UNSAFE_PortalProvider, useLocale } from "react-aria";
import { useResizeObserver } from "react-aria/private/utils/useResizeObserver";
import {
	composeRenderProps,
	OverlayTriggerStateContext,
	PopoverContext,
	Popover as PopoverPrimitive,
	useContextProps,
} from "react-aria-components";
import { useOverlayTriggerState } from "react-stately";
import { app } from "@/scripts/app";

export const Popover = memo(({
	ref,
	...props
}: ComponentProps<typeof PopoverPrimitive>) => {
	[props, ref] = useContextProps(
		mergeProps(
			{
				shouldUpdatePosition: false,
			} satisfies ComponentProps<typeof PopoverPrimitive>,
			props,
		),
		ref,
		PopoverContext,
	);

	const overlay_trigger_state_context = use(OverlayTriggerStateContext);
	const overlay_trigger_state = useOverlayTriggerState(props);

	const state = "boolean" === typeof props.isOpen || "boolean" === typeof props.defaultOpen || !overlay_trigger_state_context
		? overlay_trigger_state
		: overlay_trigger_state_context;

	const {
		crossOffset = 0,
		offset = 0,
		placement = "bottom",
		triggerRef,
	} = props;
	const { isOpen } = state;

	const { direction } = useLocale();

	const [floating_style, set_floating_style] = useState<CSSProperties | undefined>();
	const [render_placement, set_render_placement] = useState<Placement | undefined>();
	const [trigger_anchor_point, set_trigger_anchor_point] = useState<string | undefined>();
	const [trigger_width, set_trigger_width] = useState<string | undefined>();

	const floating_placement = useMemo(() => {
		const position = placement.split("\x20", 2);

		switch (direction) {
			case "ltr": {
				const [main_axis, cross_axis] = position;

				if (main_axis) {
					position[0] = {
						end: "right",
						start: "left",
					}[main_axis] ?? main_axis;
				}

				if (cross_axis) {
					position[1] = {
						left: "start",
						right: "end",
					}[cross_axis] ?? cross_axis;
				}

				break;
			}

			case "rtl": {
				const [main_axis, cross_axis] = position;

				if (main_axis) {
					position[0] = {
						end: "left",
						start: "right",
					}[main_axis] ?? main_axis;
				}

				if (cross_axis) {
					position[1] = {
						left: "end",
						right: "start",
					}[cross_axis] ?? cross_axis;
				}

				break;
			}

			default:
		}

		return position.filter(Boolean).join("\x2D") as Placement;
	}, [direction, placement]);

	const get_container = useCallback(
		() => {
			const trigger = triggerRef?.current;
			if (trigger instanceof HTMLElement) {
				const { offsetParent } = trigger;
				if (offsetParent instanceof HTMLElement) {
					return offsetParent;
				}
			}

			return null;
		},
		[triggerRef],
	);

	const on_resize = useCallback(() => {
		const trigger = triggerRef?.current;
		if (!trigger) {
			return;
		}

		const { scale } = app.canvas.ds;
		set_trigger_width(`${trigger.getBoundingClientRect().width / scale}px`);
	}, [triggerRef]);

	useLayoutEffect(on_resize, [on_resize]);

	useResizeObserver({
		onResize: on_resize,
		ref: triggerRef,
	});

	useLayoutEffect(() => {
		if (!isOpen) {
			return;
		}

		const popover = ref.current;
		if (!popover) {
			return;
		}

		const trigger = triggerRef?.current;
		if (!trigger) {
			return;
		}

		const controller = new AbortController();

		void (async (signal: AbortSignal) => {
			try {
				const position = await computePosition(trigger, popover, {
					middleware: [
						floating_flip(),
						floating_float({
							crossAxis: crossOffset,
							mainAxis: offset,
						}),
						floating_arrow({
							element: document.createElement("div"),
						}),
					],
					placement: floating_placement,
				});

				if (signal.aborted) {
					return;
				}

				const {
					middlewareData: {
						arrow: {
							x: trigger_anchor_point_x = 0,
							y: trigger_anchor_point_y = 0,
						} = {},
					},
					placement,
					x,
					y,
				} = position;

				const [main_axis] = placement.split("\x2D", 1) as [Placement, Placement] | [Placement];

				set_render_placement(main_axis);
				set_trigger_anchor_point(`translate(${trigger_anchor_point_x}px, ${trigger_anchor_point_y}px)`);

				set_floating_style({
					left: `${x}px`,
					top: `${y}px`,
				});
			}
			catch {}
		})(controller.signal);

		return () => {
			controller.abort();
		};
	}, [crossOffset, floating_placement, isOpen, offset, ref, triggerRef]);

	useLayoutEffect(() => {
		if (!render_placement) {
			return;
		}

		const popover = ref.current;
		if (!popover) {
			return;
		}

		popover.dataset.placement = render_placement;
	}, [ref, render_placement]);

	return <UNSAFE_PortalProvider getContainer={get_container}>
		<PopoverPrimitive
			{...props}
			className={cn(
				"relative isolate z-50 w-(--trigger-width) rounded-md border border-component-node-border/10 bg-modal-panel-background shadow-md overflow-hidden origin-(--trigger-anchor-point) entering:motion-duration-100 entering:motion-opacity-in-0 entering:motion-scale-in-95 placement-bottom:entering:-motion-translate-y-in-2 exiting:motion-duration-100 exiting:motion-opacity-out-0 placement-bottom:exiting:-motion-translate-y-out-2 select-none pointer-events-auto cursor-auto",
				props.className,
			)}
			crossOffset={crossOffset}
			offset={offset}
			placement={placement}
			ref={ref}
			style={composeRenderProps(props.style, (style) => ({
				bottom: "initial",
				left: 0,
				right: "initial",
				top: 0,
				...style,
				...floating_style,
				"--trigger-anchor-point": trigger_anchor_point,
				"--trigger-width": trigger_width,
				position: "absolute" as const,
			}))}
		/>
	</UNSAFE_PortalProvider>;
});
