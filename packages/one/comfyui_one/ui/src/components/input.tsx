import type { ComponentProps, FunctionComponent } from "react";

import { Input as InputPrimitive, mergeProps } from "@base-ui/react";
import { memo, useMemo } from "react";

export const Input = memo(({
	className,
	...props
}: InputPrimitive.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<InputPrimitive.Props, "className">>>(
			{ className },
			{ className: "one:placeholder:text-muted-foreground" },
			{ className: "one:block one:h-8 one:w-full one:rounded-lg one:border-none one:bg-background one:py-0 one:px-2.5 one:text-sm one:text-current one:outline one:outline-solid one:-outline-offset-1 one:outline-input one:focus-visible:outline-ring one:ring-0 one:focus-visible:ring-3 one:ring-ring/0 one:focus-visible:ring-ring/50 one:outline-none one:disabled:opacity-50 one:transition-[background-color,box-shadow,opacity,outline-color] one:select-none one:cursor-auto" },
		),
		[className],
	));

	return <InputPrimitive
		className={className}
		{...props}
	/>;
});

export const InputSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:after:flex-none one:after:block after:h-3.5 one:after:w-6/10 one:after:rounded-md one:after:bg-muted" },
			{ className: "one:flex one:h-8 one:w-full one:rounded-lg one:bg-muted/30 one:px-2.5 one:items-center one:animate-pulse one:select-none one:pointer-events-none one:cursor-auto" },
		),
		[className],
	));

	return <div
		className={className}
		{...props}
	/>;
});
