import type { ComponentProps } from "react";

import { cn } from "cn";
import { Check, ChevronDown } from "lucide-react";
import { memo } from "react";
import {
	ComboBox as ComboBoxPrimitive,
	composeRenderProps,
	ListBoxItem as ListBoxItemPrimitive,
	ListBox as ListBoxPrimitive,
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
import { Popover } from "./popover";

export const Combobox = memo(({
	className,
	menuTrigger = "focus",
	...props
}: ComponentProps<typeof ComboBoxPrimitive>) => {
	return <ComboBoxPrimitive
		className={cn(
			"relative cursor-auto",
			className,
		)}
		menuTrigger={menuTrigger}
		{...props}
	/>;
}) as typeof ComboBoxPrimitive;

export const ComboboxSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof Combobox>, "className">) => {
	return <div
		className={cn(
			"relative cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const ComboboxContent = memo(({
	className,
	containerPadding = 0,
	offset = 6,
	...props
}: ComponentProps<typeof Popover>) => {
	return <Popover
		className={cn(
			"max-h-72 bg-modal-card-background",
			className,
		)}
		containerPadding={containerPadding}
		data-slot="combobox-content"
		isNonModal
		offset={offset}
		{...props}
	/>;
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
}: ComponentProps<typeof ListBoxItemPrimitive>) => {
	return <ListBoxItemPrimitive
		className={cn(
			"relative flex rounded-md bg-transparent hover:bg-component-node-widget-background-hovered py-1 ps-1.5 pe-8 items-center text-component-node-foreground text-xs transition-colors [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-3 [&_svg]:pointer-events-none",
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
						? <div className="absolute right-2 flex size-4 items-center justify-center opacity-70 pointer-events-none">
							<Check />
						</div>
						: null
				}
			</>)
		}
	</ListBoxItemPrimitive>;
}) as typeof ListBoxItemPrimitive;

export const ComboboxList = memo(({
	className,
	...props
}: ComponentProps<typeof ListBoxPrimitive>) => {
	return <ListBoxPrimitive
		className={cn(
			"group/combobox-content max-h-[inherit] p-1 overflow-y-auto scroll-py-1 overscroll-contain",
			className,
		)}
		data-slot="combobox-list"
		{...props}
	/>;
}) as typeof ListBoxPrimitive;
