import type { ComponentProps } from "react";
import type {
	NumberFieldProps as NumberFieldPrimitiveProps,
	SwitchFieldProps as SwitchFieldPrimitiveProps,
	TextFieldProps as TextFieldPrimitiveProps,
} from "react-aria-components";

import { cn } from "cn";
import { memo } from "react";
import {
	NumberField as NumberFieldPrimitive,
	SwitchField as SwitchFieldPrimitive,
	TextField as TextFieldPrimitive,
} from "react-aria-components";
import { Group } from "./group";
import { Label, LabelSkeleton } from "./label";

export const Field = memo(({
	className,
	...props
}: ComponentProps<typeof Group>) => {
	return <Group
		className={cn(
			"group/field flex flex-col gap-1 select-none cursor-auto",
			className,
		)}
		data-slot="field"
		role="group"
		{...props}
	/>;
});

export const FieldSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof Field>, "className">) => {
	return <div
		className={cn(
			"group/field flex flex-col gap-1 select-none cursor-auto",
			className,
		)}
		{...props}
	/>;
});


export const FieldLabel = memo(({
	className,
	...props
}: ComponentProps<typeof Label>) => {
	return <Label
		className={cn(
			"group/field-label peer/field-label w-fit leading-snug",
			className,
		)}
		data-slot="field-label"
		{...props}
	/>;
});

export const FieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof FieldLabel>, "className">) => {
	return <LabelSkeleton
		className={cn(
			"group/field-label peer/field-label w-fit",
			className,
		)}
		data-slot="field-label"
	/>;
});

export const NumberField = memo(({
	className,
	...props
}: NumberFieldPrimitiveProps) => {
	return <NumberFieldPrimitive
		className={cn(
			"group/field flex flex-col gap-1 select-none cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const NumberFieldSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof NumberField>, "className">) => {
	return <div
		className={cn(
			"group/field flex flex-col gap-1 select-none cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const SwitchField = memo(({
	className,
	...props
}: SwitchFieldPrimitiveProps) => {
	return <SwitchFieldPrimitive
		className={cn(
			"group/field flex gap-2 select-none cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const SwitchFieldSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof SwitchField>, "className">) => {
	return <div
		className={cn(
			"group/field flex gap-2 select-none cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const TextField = memo(({
	className,
	...props
}: TextFieldPrimitiveProps) => {
	return <TextFieldPrimitive
		className={cn(
			"group/field flex flex-col gap-1 select-none cursor-auto",
			className,
		)}
		{...props}
	/>;
});

export const TextFieldSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div"> & Pick<ComponentProps<typeof TextField>, "className">) => {
	return <div
		className={cn(
			"group/field flex flex-col gap-1 select-none cursor-auto",
			className,
		)}
		{...props}
	/>;
});
