import type { HTMLProps } from "@base-ui/react";
import type { ComponentProps, FunctionComponent, ReactNode, RefObject } from "react";

import { Combobox as ComboboxPrimitive, mergeProps } from "@base-ui/react";
import { CheckIcon, ChevronsUpDownIcon } from "lucide-react";
import { createContext, memo, use, useCallback, useMemo, useRef } from "react";
import { Field } from "./field";

const ComboboxRefContext = createContext<null | RefObject<HTMLDivElement | null>>(null);

export const Combobox = memo(({
	className,
	...props
}: ComboboxPrimitive.Root.Props<unknown> & Pick<ComponentProps<typeof Field>, "className">) => {
	const ref = useRef<HTMLDivElement>(null);

	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<typeof Field>, "className">>>(
			{ className },
			{ className: "one:anchor-scope-[--combobox]" },
		),
		[className],
	));

	return <ComboboxRefContext value={ref}>
		<Field
			className={className}
			data-capture-wheel
			ref={ref}
		>
			<ComboboxPrimitive.Root {...props} />
		</Field>
	</ComboboxRefContext>;
}) as <T>(props: ComboboxPrimitive.Root.Props<T> & Pick<ComponentProps<typeof Field>, "className">) => ReactNode;

export const ComboboxContent = memo(({
	align = "center",
	className,
	side = "bottom",
	...props
}: ComboboxPrimitive.Popup.Props & Pick<ComboboxPrimitive.Positioner.Props, "align" | "side">) => {
	const root_ref = use(ComboboxRefContext);

	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComboboxPrimitive.Popup.Props, "className">>>(
			{ className },
			{ className: "one:max-h-40 one:rounded-lg one:bg-popover one:text-sm one:text-popover-foreground one:overflow-y-auto one:overflow-x-clip one:outline one:outline-solid one:-outline-offset-1 one:outline-border one:shadow-md one:closed:motion-opacity-out-0 one:open:motion-opacity-in-0 one:closed:motion-scale-out-95 one:open:motion-scale-in-95 one:side-bottom:open:motion-translate-y-in-[-8px] one:side-left:open:motion-translate-x-in-[8px] one:side-top:open:motion-translate-y-in-[8px] one:side-right:open:motion-translate-x-in-[-8px] one:motion-duration-150" },
		),
		[className],
	));

	const render = useCallback(
		(props: HTMLProps) =>
			<div
				{...props}
				style={undefined}
			/>,
		[],
	);

	return <ComboboxPrimitive.Portal container={root_ref}>
		<ComboboxPrimitive.Positioner
			align={align}
			alignOffset={0}
			className="one:isolate one:absolute one:z-50 one:side-inline:align-center:[align-self:anchor-center] one:position-anchor-[--combobox] one:side-inline:align-start:inset-bs-[anchor(self-start)] one:side-inline:align-end:inset-be-[anchor(self-end)] one:side-inline-end:inset-s-[anchor(self-end)] one:side-inline-start:inset-e-[anchor(self-start)] one:side-x:align-start:top-[anchor(top)] one:side-x:align-center:top-[anchor(center)] one:side-bottom:top-[anchor(bottom)] one:side-y:align-end:right-[anchor(right)] one:side-left:right-[anchor(left)] one:side-x:align-end:bottom-[anchor(bottom)] one:side-top:bottom-[anchor(top)] one:side-y:align-start:left-[anchor(left)] one:side-y:align-center:left-[anchor(center)] one:side-right:left-[anchor(right)] one:side-inline-end:ms-1 one:side-inline-start:me-1 one:side-bottom:mt-1 one:side-top:mb-1 one:side-right:ml-1 one:side-left:mr-1 one:w-[anchor-size(width)] one:side-x:align-center:-translate-y-1/2 one:side-y:align-center:-translate-x-1/2"
			collisionPadding={0}
			data-align={align}
			data-side={side}
			disableAnchorTracking
			render={render}
			side={side}
			sideOffset={0}
		>
			<ComboboxPrimitive.Popup
				className={className}
				{...props}
				data-align={align}
				data-side={side}
			/>
		</ComboboxPrimitive.Positioner>
	</ComboboxPrimitive.Portal>;
});

export const ComboboxInput = memo(({
	className,
	...props
}: Omit<ComboboxPrimitive.Input.Props, "className"> & Pick<ComboboxPrimitive.InputGroup.Props, "className">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComboboxPrimitive.InputGroup.Props, "className">>>(
			{ className },
			{ className: "one:anchor-[--combobox] one:flex one:h-8 one:rounded-lg one:bg-background one:has-[button]:pe-1 one:items-center one:justify-between one:overflow-clip one:outline one:outline-solid one:-outline-offset-1 one:outline-input one:focus-within:outline-ring one:ring-0 one:focus-within:ring-3 one:ring-ring/0 one:focus-within:ring-ring/50 one:disabled:opacity-50 one:transition-[background-color,box-shadow,opacity,outline-color] one:select-none one:cursor-auto" },
		),
		[className],
	));

	return <ComboboxPrimitive.InputGroup className={className}>
		<ComboboxPrimitive.Input
			className="one:flex-auto one:h-full one:rounded-s-lg one:border-none one:bg-transparent one:py-0 one:ps-2.5 one:pe-1 one:text-sm one:text-current one:outline-none one:cursor-auto"
			{...props}
		/>
		<ComboboxPrimitive.Trigger className="one:flex-none one:flex one:size-6 one:rounded-lg one:border-none one:bg-transparent one:hover:bg-muted one:p-0 one:items-center one:justify-center one:text-muted-foreground one:hover:text-current one:outline-none one:active:scale-95 one:transition-[background-color,color,scale] one:cursor-auto">
			<ChevronsUpDownIcon className="one:flex-none one:block one:size-3 one:pointer-events-none" />
		</ComboboxPrimitive.Trigger>
	</ComboboxPrimitive.InputGroup>;
});

export const ComboboxInputSkeleton = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:after:flex-none one:after:mx-2.5 one:after:block one:after:h-3.5 one:after:w-4/10 one:after:rounded-md one:after:bg-muted" },
			{ className: "one:flex one:h-8 one:rounded-lg one:bg-background one:pe-1 one:items-center one:justify-between one:overflow-clip one:animate-pulse one:select-none one:pointer-events-none one:cursor-auto" },
		),
		[className],
	));

	return <div
		className={className}
		{...props}
	>
		<ChevronsUpDownIcon className="one:order-last one:mx-1.5 one:block one:size-3 one:text-muted" />
	</div>;
});

export const ComboboxItem = memo(({
	children,
	className,
	...props
}: ComboboxPrimitive.Item.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComboboxPrimitive.Item.Props, "className">>>(
			{ className },
			{ className: "one:flex one:h-8 one:w-full one:rounded-md one:border-none one:bg-transparent one:hover:bg-accent one:py-0 one:px-1.5 one:items-center one:justify-between one:gap-1 one:text-start one:text-sm one:text-current one:hover:text-accent-foreground one:outline-none one:transition-colors one:cursor-auto" },
		),
		[className],
	));

	const render = useCallback((props: HTMLProps) => <button {...props} />, []);

	return <ComboboxPrimitive.Item
		className={className}
		nativeButton
		render={render}
		{...props}
	>
		<span
			children={children}
			className="one:flex-auto one:block one:pointer-events-none"
		/>
		<ComboboxPrimitive.ItemIndicator className="one:-me-1.5 one:flex-none one:flex one:size-6 one:items-center one:justify-center one:pointer-events-none">
			<CheckIcon className="one:flex-none one:block one:size-3" />
		</ComboboxPrimitive.ItemIndicator>
	</ComboboxPrimitive.Item>;
});

export const ComboboxList = memo(({
	className,
	...props
}: ComboboxPrimitive.List.Props) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComboboxPrimitive.List.Props, "className">>>(
			{ className },
			{ className: "one:rounded-lg one:p-1" },
		),
		[className],
	));

	return <ComboboxPrimitive.List
		className={className}
		{...props}
	/>;
});
