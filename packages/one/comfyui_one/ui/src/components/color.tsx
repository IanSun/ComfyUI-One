import type { BaseUIEvent } from "@base-ui/react";
import type { PlainColorObject } from "colorjs.io";
import type { ClipboardEvent, ComponentProps, FocusEvent, FunctionComponent, KeyboardEvent } from "react";

import {
	Field as FieldPrimitive,
	Input as InputPrimitive,
	mergeProps,
	NumberField as NumberFieldPrimitive,
} from "@base-ui/react";
import { useIsoLayoutEffect } from "@base-ui/utils/useIsoLayoutEffect";
import {
	clone as clone_color,
	ColorSpace,
	getColor as get_color,
	get as get_color_prop,
	serialize as serialize_color,
	set as set_color_prop,
	sRGB,
	to as to_color,
} from "colorjs.io/fn";
import { createContext, memo, use, useCallback, useMemo, useRef, useState } from "react";

ColorSpace.register(sRGB);

const ColorFieldRootContext = createContext<{
	set_value_as_color: (value: null | PlainColorObject) => void;
	value_as_color: null | PlainColorObject;
} | null>(null);

const useColorFieldRootContext = () => {
	const context = use(ColorFieldRootContext);
	return context!;
};

export const ColorAlphaInput = memo(({
	className,
	...props
}: Omit<NumberFieldPrimitive.Root.Props, "defaultValue" | "onValueChange" | "onValueCommitted" | "value">) => {
	const {
		set_value_as_color,
		value_as_color,
	} = useColorFieldRootContext();

	const value = useMemo(
		(): null | number => value_as_color ? get_color_prop(value_as_color, "alpha") * 1e2 : null,
		[value_as_color],
	);

	const on_value_change = useCallback(
		(value: null | number): void => {
			const color = "number" === typeof value && !Number.isNaN(value) && value_as_color
				? set_color_prop(clone_color(value_as_color), "alpha", value / 1e2)
				: null;
			set_value_as_color(color);
		},
		[value_as_color, set_value_as_color],
	);

	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<NumberFieldPrimitive.Root.Props, "className">>>(
			{ className },
			{ className: "one:flex one:h-8 one:min-w-24 one:rounded-lg one:bg-background one:items-center one:justify-between one:overflow-clip one:outline one:outline-solid one:-outline-offset-1 one:outline-input one:focus-within:outline-ring one:ring-0 one:focus-within:ring-3 one:ring-ring/0 one:focus-within:ring-ring/50 one:disabled:opacity-50 one:transition-[background-color,box-shadow,opacity,outline-color] one:select-none one:cursor-auto" },
		),
		[className],
	));

	return <NumberFieldPrimitive.Root
		className={className}
		format={{
			maximumFractionDigits: 0,
			useGrouping: false,
		}}
		max={100}
		min={0}
		onValueChange={on_value_change}
		role="group"
		smallStep={1}
		value={value}
		{...props}
	>
		<div className="one:flex-none one:flex one:h-full one:ps-2.5 one:pe-0.5 one:items-center one:justify-center one:text-sm one:text-muted-foreground">
			{"\x23"}
		</div>
		<NumberFieldPrimitive.Input className="one:flex-auto one:block one:h-full one:min-w-0 one:rounded-e-lg one:border-none one:bg-transparent one:py-0 one:px-1 one:text-end one:text-sm one:text-current one:outline-none one:cursor-auto" />
		<div className="one:flex-none one:flex one:h-full one:ps-0.5 one:pe-2.5 one:items-center one:justify-center one:text-sm one:text-muted-foreground">
			{"\x25"}
		</div>
	</NumberFieldPrimitive.Root>;
});

export const ColorControlGroup = memo(({
	className,
	...props
}: ComponentProps<"div">) => {
	({ className } = useMemo(
		() => mergeProps<FunctionComponent<Pick<ComponentProps<"div">, "className">>>(
			{ className },
			{ className: "one:flex one:items-center one:gap-2" },
		),
		[className],
	));

	return <div
		className={className}
		role="group"
		{...props}
	/>;
});

export const ColorField = memo(({
	className,
	defaultValue,
	format = "hexa",
	onValueChange,
	value,
	...props
}: {
	defaultValue?: string;
	format?: "hex" | "hexa";
	onValueChange?: (value: string) => void;
	value?: string;
} & FieldPrimitive.Root.Props) => {
	const value_as_color = useMemo(
		() => {
			if (value) {
				try {
					return get_color(value);
				}
				catch {}
			}
			return null;
		},
		[value],
	);

	const set_value_as_color_callback = useCallback(
		(value: null | PlainColorObject): void => {
			onValueChange?.(format_color(value, format));
		},
		[
			format,
			onValueChange,
		],
	);

	const context_value = useMemo(
		() => ({
			set_value_as_color: set_value_as_color_callback,
			value_as_color,
		}),
		[value_as_color, set_value_as_color_callback],
	);

	return <ColorFieldRootContext value={context_value}>
		<FieldPrimitive.Root
			className={className}
			{...props}
		/>
	</ColorFieldRootContext>;
});

export const ColorHexInput = memo(({
	className,
	...props
}: FieldPrimitive.Root.Props) => {
	const {
		set_value_as_color,
		value_as_color,
	} = useColorFieldRootContext();

	const allow_input_sync_ref = useRef(true);
	const input_ref = useRef<HTMLInputElement>(null);

	const [input_value, set_input_value] = useState(() => format_color_as_hex(value_as_color));

	const on_blur = useCallback(
		(event: BaseUIEvent<FocusEvent<HTMLInputElement>>): void => {
			if (event.defaultPrevented) {
				return;
			}

			const { target } = event.nativeEvent;

			if (!(target instanceof HTMLInputElement) || target.disabled || target.readOnly) {
				return;
			}

			const had_manual_input = !allow_input_sync_ref.current;

			allow_input_sync_ref.current = true;

			const committed = had_manual_input
				? parse_color_from_hex(value_as_color, target.value.trim())
				: value_as_color;

			if (had_manual_input && !committed) {
				const canonical_text = format_color_as_hex(value_as_color);
				if (input_value !== canonical_text) {
					set_input_value(canonical_text);
				}
				return;
			}

			const should_update_value = committed && format_color(value_as_color) !== format_color(committed);
			const should_commit = had_manual_input || should_update_value;
			if (should_commit) {
				set_value_as_color(committed);
			}

			const canonical_text = format_color_as_hex(committed);
			if (input_value !== canonical_text) {
				set_input_value(canonical_text);
			}
		},
		[input_value, value_as_color, set_value_as_color],
	);

	const on_input_value_change = useCallback(
		(value: string): void => {
			value = value.replaceAll(/[^0-9a-fA-F]/gu, "").slice(0, 6);

			allow_input_sync_ref.current = false;

			set_input_value(value);

			const { length } = value;
			if (0 < length && 3 !== length && 6 !== length) {
				return;
			}

			const color = parse_color_from_hex(value_as_color, value);

			if (color) {
				set_value_as_color(color);
			}
		},
		[value_as_color, set_value_as_color],
	);

	const on_key_down = useCallback(
		(event: BaseUIEvent<KeyboardEvent<HTMLInputElement>>): void => {
			if (event.defaultPrevented) {
				return;
			}

			const { target } = event.nativeEvent;

			if (!(target instanceof HTMLInputElement) || target.disabled || target.readOnly) {
				return;
			}

			const { key } = event;

			if ((/^[\x30-\x39\x41-\x46\x61-\x66]$/u).test(key)) {
				const current_length = target.value.trim().length;
				if (6 <= current_length || 3 === current_length) {
					event.preventDefault();
					event.stopPropagation();
				}
				return;
			}

			if (
				event.altKey
				|| event.ctrlKey
				|| event.metaKey
				|| (/^(?:ArrowLeft|ArrowRight|Backspace|Delete|Enter|Escape|Tab|[\x30-\x39\x41-\x46\x61-\x66])$/u).test(key)
			) {
				return;
			}

			event.preventDefault();
			event.stopPropagation();

			const value_as_number = Number.parseInt(target.value.trim(), 16);
			if (Number.isNaN(value_as_number)) {
				return;
			}

			const next_value_as_number = ((): number => {
				switch (key) {
					case "ArrowDown": {
						allow_input_sync_ref.current = true;
						return value_as_number - 1;
					}

					case "ArrowUp": {
						allow_input_sync_ref.current = true;
						return value_as_number + 1;
					}

					case "End": {
						allow_input_sync_ref.current = true;
						return 0xFF_FF_FF;
					}

					case "Home": {
						allow_input_sync_ref.current = true;
						return 0;
					}

					default: {
						return value_as_number;
					}
				}
			})();

			const next_clamp_value_as_number = Math.max(0, Math.min(0xFF_FF_FF, next_value_as_number));
			if (value_as_number === next_clamp_value_as_number) {
				return;
			}

			const next_value = next_clamp_value_as_number.toString(16).padStart(6, "0");
			const color = parse_color_from_hex(value_as_color, next_value);
			if (color) {
				set_value_as_color(color);
				set_input_value(next_value);
			}
		},
		[value_as_color, set_value_as_color],
	);

	const on_paste = useCallback(
		(event: BaseUIEvent<ClipboardEvent<HTMLInputElement>>): void => {
			if (event.defaultPrevented) {
				return;
			}

			const { target } = event.nativeEvent;

			if (!(target instanceof HTMLInputElement) || target.disabled || target.readOnly) {
				return;
			}

			const value = (() => {
				try {
					return event.clipboardData.getData("text/plain").trim();
				}
				catch {}
				return "";
			})();

			const color = (() => {
				try {
					return to_color(value, sRGB);
				}
				catch {
					try {
						return to_color(`\x23${value}`, sRGB);
					}
					catch {}
				}
				return null;
			})();

			if (!color) {
				return;
			}

			event.preventDefault();

			allow_input_sync_ref.current = true;

			set_value_as_color(color);
			set_input_value(format_color_as_hex(color));
		},
		[set_value_as_color],
	);

	useIsoLayoutEffect(() => {
		if (allow_input_sync_ref.current) {
			const canonical = format_color_as_hex(value_as_color);
			if (input_value !== canonical) {
				set_input_value(canonical);
			}
		}
	}, [input_value, value_as_color]);

	({ className, ...props } = useMemo(
		() => mergeProps<FunctionComponent<FieldPrimitive.Root.Props>>(
			{
				className,
				...props,
			},
			{ className: "one:flex one:h-8 one:min-w-24 one:rounded-lg one:bg-background one:items-center one:justify-between one:overflow-clip one:outline one:outline-solid one:-outline-offset-1 one:outline-input one:focus-within:outline-ring one:ring-0 one:focus-within:ring-3 one:ring-ring/0 one:focus-within:ring-ring/50 one:disabled:opacity-50 one:transition-[background-color,box-shadow,opacity,outline-color] one:select-none one:cursor-text one:disabled:cursor-auto" },
			{
				onClick: () => {
					input_ref.current?.focus();
				},
			},
		),
		[className, props],
	));

	return <FieldPrimitive.Root
		className={className}
		role="group"
		{...props}
	>
		<div className="one:flex-none one:flex one:h-full one:ps-2.5 one:pe-0.5 one:items-center one:justify-center one:text-sm one:text-muted-foreground one:pointer-events-none">
			{"\x23"}
		</div>
		<InputPrimitive
			className="one:flex-auto one:h-full one:min-w-0 one:rounded-e-lg one:border-none one:bg-transparent one:py-0 one:ps-1 one:pe-2.5 one:text-sm one:text-current one:outline-none one:cursor-auto"
			onBlur={on_blur}
			onKeyDown={on_key_down}
			onPaste={on_paste}
			onValueChange={on_input_value_change}
			ref={input_ref}
			value={input_value}
		/>
	</FieldPrimitive.Root>;
});

function format_color(value: null | PlainColorObject, format: "hex" | "hexa" = "hexa"): string {
	if (value) {
		try {
			return serialize_color(
				value,
				{
					alpha: "hexa" === format,
					collapse: false,
					format: "hex",
					inGamut: true,
				},
			)
				.toUpperCase();
		}
		catch {}
	}
	return "";
}

function format_color_as_hex(value: null | PlainColorObject): string {
	if (value) {
		const hex = serialize_color(
			value,
			{
				alpha: false,
				collapse: false,
				format: "hex",
				inGamut: true,
			},
		);
		return hex.slice(1).toUpperCase();
	}
	return "";
}

function parse_color_from_hex(color: null | PlainColorObject, value: string): null | PlainColorObject {
	if (color && [3, 6].includes(value.length)) {
		try {
			const hex_color = to_color(`\x23${value}`, sRGB);
			const alpha = get_color_prop(color, "alpha");
			return set_color_prop(hex_color, "alpha", alpha);
		}
		catch {}
	}
	return null;
}
