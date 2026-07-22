import type { zFloatInputOptions, zIntInputOptions } from "@comfyorg/object-info-parser";
import type { z } from "zod";

import { memo, Suspense } from "react";
import {
	FieldLabel,
	FieldLabelGroup,
	FieldLabelSkeleton,
	FieldSkeleton,
	InputSkeleton,
	NumberFieldInput,
	NumberField as NumberFieldPrimitive,
	NumberFieldScrubArea,
} from "../components";
import {
	useNodeDOMWidgetContext,
	useNodeDOMWidgetOnValueChange,
	useNodeDOMWidgetValue,
	useNodeInputTranslation,
} from "../hooks";

export const Number = memo(() => {
	return <Suspense fallback={<NumberSkeleton />}>
		<NumberField />
	</Suspense>;
});

const NumberSkeleton = memo(() => {
	return <FieldSkeleton>
		<FieldLabelSkeleton />
		<InputSkeleton />
	</FieldSkeleton>;
});

const NumberField = memo(() => {
	const {
		specification: {
			max = Infinity,
			min = -Infinity,
			step = 1,
		},
	} = useNodeDOMWidgetContext<number, z.infer<typeof zFloatInputOptions | typeof zIntInputOptions>>();
	const value = useNodeDOMWidgetValue<number>();
	const on_value_change = useNodeDOMWidgetOnValueChange<number>();

	return <NumberFieldPrimitive
		max={max}
		min={min}
		onValueChange={on_value_change}
		step={step}
		value={value}
	>
		<FieldLabelGroup>
			<NumberFieldLabel />
			<NumberFieldScrubArea />
		</FieldLabelGroup>
		<NumberFieldInput />
	</NumberFieldPrimitive>;
});

const NumberFieldLabel = memo(() => {
	const t = useNodeInputTranslation();
	const { specification } = useNodeDOMWidgetContext<number, z.infer<typeof zFloatInputOptions | typeof zIntInputOptions>>();

	return <FieldLabel>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});
