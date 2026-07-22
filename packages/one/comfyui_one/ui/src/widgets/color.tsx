import type { ColorInputSpec } from "@comfyorg/object-info-parser/schemas/nodeDefSchemaV2";

import { memo, Suspense } from "react";
import {
	ColorAlphaInput,
	ColorControlGroup,
	ColorField as ColorFieldPrimitive,
	ColorHexInput,
	FieldLabel,
	FieldLabelSkeleton,
	FieldSkeleton,
	InputSkeleton,
} from "../components";
import {
	useNodeDOMWidgetContext,
	useNodeDOMWidgetOnValueChange,
	useNodeDOMWidgetValue,
	useNodeInputTranslation,
} from "../hooks";

type ColorSpec = { options?: { format?: "hex" | "hexa" } } & ColorInputSpec;

export const Color = memo(() => {
	return <Suspense fallback={<ColorSkeleton />}>
		<ColorField />
	</Suspense>;
});

const ColorSkeleton = memo(() => {
	<FieldSkeleton>
		<FieldLabelSkeleton />
		<InputSkeleton />
	</FieldSkeleton>;
});

const ColorField = memo(() => {
	const { specification: { options } } = useNodeDOMWidgetContext<string, ColorSpec>();
	const value = useNodeDOMWidgetValue<string>();
	const on_value_change = useNodeDOMWidgetOnValueChange<string>();

	return <ColorFieldPrimitive
		format={options?.format}
		onValueChange={on_value_change}
		value={value}
	>
		<ColorFieldLabel />
		<ColorControlGroup>
			<ColorHexInput className="one:flex-4" />
			<ColorAlphaInput className="one:flex-3" />
		</ColorControlGroup>
	</ColorFieldPrimitive>;
});

const ColorFieldLabel = memo(() => {
	const t = useNodeInputTranslation();
	const { specification } = useNodeDOMWidgetContext<string, ColorSpec>();

	return <FieldLabel>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});
