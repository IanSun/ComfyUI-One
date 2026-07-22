import type { ComponentProps, FunctionComponent } from "react";

import { Field as FieldPrimitive, mergeProps } from "@base-ui/react";
import { memo, useMemo } from "react";

export const Field = memo(({
	className,
	...props
}: FieldPrimitive.Root.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<FieldPrimitive.Root.Props, "className">>>(
			{ className },
			{ className: "one:mb-2 one:select-none one:cursor-auto" },
		),
		[className],
	));

	return <FieldPrimitive.Root
		className={className}
		{...props}
	/>;
});

export const FieldSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:mb-2 one:select-none one:pointer-events-none one:cursor-auto" },
		),
		[className],
	));

	return <div
		className={className}
		{...props}
	/>;
});

export const FieldLabel = memo(({
	className,
	...props
}: FieldPrimitive.Label.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<FieldPrimitive.Label.Props, "className">>>(
			{ className },
			{ className: "one:mb-2 one:group-has-[*]/field-label:mb-0 one:group-has-[*]/field-label:flex-auto one:block one:text-sm one:font-medium one:select-none one:cursor-auto" },
		),
		[className],
	));

	return <FieldPrimitive.Label
		className={className}
		{...props}
	/>;
});

export const FieldLabelSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:after:flex-none one:after:block one:after:h-3.5 one:after:max-w-full one:after:w-20 one:after:rounded-md one:after:bg-muted" },
			{ className: "one:mb-2 one:group-has-[*]/field-label:mb-0 one:group-has-[*]/field-label:flex-auto one:flex one:h-5 one:items-center one:animate-pulse one:select-none one:pointer-events-none one:cursor-auto" },
		),
		[className],
	));

	return <div
		className={className}
		{...props}
	/>;
});

export const FieldLabelGroup = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:group/field-label one:mb-2 one:flex one:items-center one:gap-2" },
		),
		[className],
	));

	return <div
		className={className}
		{...props}
	/>;
});
