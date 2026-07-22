import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import { Button, ButtonSkeleton } from "./button";
import { Group } from "./group";
import { Input, InputSkeleton } from "./input";

export const InputGroup = memo(({
	className,
	...props
}: ComponentProps<typeof Group>) => {
	return <Group
		className={cn(
			"group/input-group flex h-6 rounded-md border-none bg-component-node-widget-background has-[>[data-align=inline-end]]:[&>input]:pe-1 has-[>[data-align=inline-start]]:[&>input]:ps-1 items-center ring-0 has-[[data-slot=input-group-control]:focus-visible]:ring has-[[data-slot=input-group-control]:focus-visible]:ring-component-node-widget-background-highlighted transition-shadow cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const InputGroupSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof InputGroup>, "className">) => {
	return <div
		className={cn(
			"group/input-group flex h-6 rounded-md border-none bg-component-node-widget-background has-[>[data-align=inline-end]]:[&>input]:pe-1 has-[>[data-align=inline-start]]:[&>input]:ps-1 items-center cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const InputGroupAddon = memo(({
	align = "inline-start",
	className,
	...props
}: { align?: "inline-end" | "inline-start" } & ComponentProps<"div">) => {
	return <div
		className={cn(
			"data-[align=inline-start]:order-first data-[align=inline-end]:order-last flex py-0.5 data-[align=inline-start]:ps-0.5 data-[align=inline-end]:pe-0.5 items-center justify-center text-sm [&>svg:not([class*='size-'])]:size-4",
			className,
		)}
		data-align={align}
		data-slot="input-group-addon"
		onClick={(event) => {
			if ((event.target as HTMLElement).closest("button")) {
				return;
			}
			event.currentTarget.parentElement?.querySelector("input")?.focus();
		}}
		role="group"
		{...props}
	/>;
});

export const InputGroupAddonSkeleton = memo(({
	align = "inline-start",
	className,
	...props
}: ComponentProps<typeof InputGroupAddon>) => {
	return <div
		className={cn(
			"data-[align=inline-start]:order-first data-[align=inline-end]:order-last flex py-0.5 data-[align=inline-start]:ps-0.5 data-[align=inline-end]:pe-0.5 items-center justify-center",
			className,
		)}
		data-align={align}
		data-slot="input-group-addon"
		role="group"
		{...props}
	/>;
});

export const InputGroupButton = memo(({
	className,
	size = "default",
	type = "button",
	variant = "ghost",
	...props
}: { size?: "default" | "icon" } & ComponentProps<typeof Button>) => {
	return <Button
		className={cn(
			"flex h-5 data-[size=icon]:w-5",
			className,
		)}
		data-size={size}
		type={type}
		variant={variant}
		{...props}
	/>;
});

export const InputGroupButtonSkeleton = memo(({
	className,
	size = "default",
	variant = "ghost",
	...props
}: Pick<ComponentProps<typeof ButtonSkeleton>, "children"> & Pick<ComponentProps<typeof InputGroupButton>, "className" | "size" | "variant">) => {
	return <ButtonSkeleton
		className={cn(
			"flex h-6 data-[size=icon]:w-6",
			className,
		)}
		data-size={size}
		variant={variant}
		{...props}
	/>;
});

export const InputGroupInput = memo(({
	className,
	...props
}: ComponentProps<typeof Input>) => {
	return <Input
		className={cn(
			"flex-1 rounded-none bg-transparent focus:ring-0 focus-visible:ring-0",
			className,
		)}
		data-slot="input-group-control"
		{...props}
	/>;
});

export const InputGroupInputSkeleton = memo(({
	className,
	...props
}: Pick<ComponentProps<typeof InputGroupInput>, "className">) => {
	return <InputSkeleton
		className={cn(
			"flex-1 rounded-none bg-transparent",
			className,
		)}
		data-slot="input-group-control"
		{...props}
	/>;
});
