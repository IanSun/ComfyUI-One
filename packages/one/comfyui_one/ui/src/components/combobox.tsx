import type { ComponentProps, FunctionComponent, NamedExoticComponent } from "react";
import type {
	ComboBoxProps as ComboBoxPrimitiveProps,
	ListBoxItemProps as ListBoxItemPrimitiveProps,
	ListBoxProps as ListBoxPrimitiveProps,
	PopoverProps as PopoverPrimitiveProps,
} from "react-aria-components";

import { useResizeObserver } from "@react-aria/utils";
import { cn } from "cn";
import { Check, ChevronDown } from "lucide-react";
import { memo, useRef, useState } from "react";
import { UNSAFE_PortalProvider } from "react-aria";
import {
	ComboBox as ComboBoxPrimitive,
	composeRenderProps,
	ListBoxItem as ListBoxItemPrimitive,
	ListBox as ListBoxPrimitive,
	Popover as PopoverPrimitive,
} from "react-aria-components";
import {
	InputGroup,
	InputGroupAddon,
	InputGroupAddonSkeleton,
	InputGroupButton,
	InputGroupButtonSkeleton,
	InputGroupInput,
	InputGroupInputSkeleton,
	InputGroupSkeleton,
} from "./input-group";

export const Combobox = memo(({
	className,
	menuTrigger = "focus",
	...props
}: ComboBoxPrimitiveProps<unknown>) => {
	return <ComboBoxPrimitive
		className={cn("cursor-auto", className)}
		menuTrigger={menuTrigger}
		{...props}
	/>;
}) as (
	NamedExoticComponent<ComboBoxPrimitiveProps<unknown>>
	& (<T>(
		this: ThisParameterType<FunctionComponent<ComboBoxPrimitiveProps<T>>>,
		...args: Parameters<FunctionComponent<ComboBoxPrimitiveProps<T>>>
	) => ReturnType<FunctionComponent<ComboBoxPrimitiveProps<T>>>)
);

export const ComboboxSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof Combobox>, "className">) => {
	return <div
		className={cn("cursor-auto", className)}
		{...props}
	/>;
});

export const ComboboxContent = memo(({
	className,
	offset = 6,
	style,
	...props
}: PopoverPrimitiveProps) => {
	const ref = useRef<HTMLDivElement>(null);

	useResizeObserver({
		ref,
		onResize: () => {
			const { current } = ref;

			if (current) {
				set_trigger_width(current.offsetWidth);
			}
		},
	});

	const [trigger_width, set_trigger_width] = useState(0);

	return <UNSAFE_PortalProvider getContainer={() => ref.current}>
		<div
			className="relative"
			ref={ref}
		/>
		<PopoverPrimitive
			className={cn(
				"relative isolate z-50 max-h-72 w-(--trigger-width) rounded-md bg-component-node-widget-background/80 backdrop-blur-sm shadow-md overflow-hidden origin-(--trigger-anchor-point) entering:motion-duration-100 entering:motion-opacity-in-0 entering:motion-scale-in-95 placement-bottom:entering:-motion-translate-y-in-2 exiting:motion-duration-100 exiting:motion-opacity-out-0 placement-bottom:exiting:-motion-translate-y-out-2",
				className,
			)}
			containerPadding={0}
			data-slot="combobox-content"
			offset={offset}
			shouldFlip={false}
			style={composeRenderProps(style, (style) => ({
				...style,
				"--trigger-width": `${trigger_width}px`,
			}))}
			{...props}
		/>
	</UNSAFE_PortalProvider>;
});

export const ComboboxInput = memo(({
	children,
	className,
	...props
}: Omit<ComponentProps<typeof InputGroupInput>, "className"> & Pick<ComponentProps<typeof InputGroup>, "className">) => {
	return <InputGroup className={cn("w-auto", className)}>
		<InputGroupInput {...props} />
		<InputGroupAddon align="inline-end">
			<InputGroupButton
				data-slot="combobox-trigger"
				size="icon"
			>
				<ChevronDown />
			</InputGroupButton>
		</InputGroupAddon>
		{children}
	</InputGroup>;
});

export const ComboboxInputSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof ComboboxInput>, "className">) => {
	return <InputGroupSkeleton className={cn("w-auto", className)}>
		<InputGroupInputSkeleton />
		<InputGroupAddonSkeleton align="inline-end">
			<InputGroupButtonSkeleton
				data-slot="combobox-trigger"
				size="icon"
			>
				<ChevronDown />
			</InputGroupButtonSkeleton>
		</InputGroupAddonSkeleton>
	</InputGroupSkeleton>;
});

export const ComboboxItem = memo(({
	children,
	className,
	...props
}: ListBoxItemPrimitiveProps) => {
	return <ListBoxItemPrimitive
		className={cn(
			"relative flex rounded-md bg-transparent data-focused:bg-component-node-widget-background-hovered py-1 ps-1.5 pe-8 items-center text-xs transition-colors [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 [&_svg]:pointer-events-none",
			className,
		)}
		data-slot="combobox-item"
		{...props}
	>
		{
			composeRenderProps(children, (children, { isSelected }) => <>
				{children}
				{
					isSelected
						? <div className="absolute right-2 flex size-4 items-center justify-center pointer-events-none">
							<Check />
						</div>
						: null
				}
			</>)
		}
	</ListBoxItemPrimitive>;
}) as (
	NamedExoticComponent<ListBoxItemPrimitiveProps<unknown>>
	& (<T>(
		this: ThisParameterType<FunctionComponent<ListBoxItemPrimitiveProps<T>>>,
		...args: Parameters<FunctionComponent<ListBoxItemPrimitiveProps<T>>>
	) => ReturnType<FunctionComponent<ListBoxItemPrimitiveProps<T>>>)
);

export const ComboboxList = memo(({
	className,
	...props
}: ListBoxPrimitiveProps<unknown>) => {
	return <ListBoxPrimitive
		className={cn(
			"group/combobox-content max-h-[inherit] p-1 overflow-y-auto scroll-py-1 overscroll-contain",
			className,
		)}
		data-slot="combobox-list"
		{...props}
	/>;
}) as (
	NamedExoticComponent<ListBoxPrimitiveProps<unknown>>
	& (<T>(
		this: ThisParameterType<FunctionComponent<ListBoxPrimitiveProps<T>>>,
		...args: Parameters<FunctionComponent<ListBoxPrimitiveProps<T>>>
	) => ReturnType<FunctionComponent<ListBoxPrimitiveProps<T>>>)
);
