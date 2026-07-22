import type { HTMLProps } from "@base-ui/react";
import type { ComponentProps, FunctionComponent } from "react";

import { mergeProps, Switch as SwitchPrimitive } from "@base-ui/react";
import { memo, useCallback, useMemo } from "react";

export const Switch = memo(({
	className,
	...props
}: SwitchPrimitive.Root.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<SwitchPrimitive.Root.Props, "className">>>(
			{ className },
			{ className: "one:flex-none one:inline-flex one:h-5 one:w-9 one:rounded-full one:border-none one:bg-input one:checked:bg-primary one:overflow-clip one:p-0.5 one:items-center one:inset-ring-0 one:focus-visible:inset-ring one:inset-ring-input one:focus-visible:inset-ring-ring one:ring one:focus-visible:ring-3 one:ring-input one:focus-visible:ring-ring/50 one:outline-none one:disabled:opacity-50 one:transition-[background-color,box-shadow,opacity] one:select-none one:cursor-auto" },
		),
		[className],
	));

	const render = useCallback((props: HTMLProps) => <button {...props} />, []);

	return <SwitchPrimitive.Root
		className={className}
		nativeButton
		render={render}
		{...props}
	>
		<SwitchPrimitive.Thumb className="one:flex-none one:block one:size-4 one:rounded-full one:bg-foreground one:translate-x-0 one:checked:translate-x-4 one:transition-transform one:pointer-events-none" />
	</SwitchPrimitive.Root>;
});

export const SwitchSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:after:flex-none one:after:block one:after:size-4 one:after:rounded-full one:after:bg-background/30" },
			{ className: "one:flex-none one:inline-flex one:h-5 one:w-9 one:rounded-full one:bg-muted/30 one:overflow-clip one:p-0.5 one:items-center one:animate-pulse one:select-none one:pointer-events-none one:cursor-auto" },
		),
		[className],
	));

	return <div
		className={className}
		{...props}
	/>;
});
