import type { zStringInputOptions } from "@comfyorg/object-info-parser";
import type { z } from "zod";

import { memo, Suspense } from "react";
import {
	Field,
	FieldLabel,
	FieldLabelSkeleton,
	FieldSkeleton,
	Input,
	InputSkeleton,
	Textarea,
	TextareaSkeleton,
} from "../components";
import {
	useNodeDOMWidgetContext,
	useNodeDOMWidgetOnValueChange,
	useNodeDOMWidgetValue,
	useNodeInputTranslation,
} from "../hooks";

export const String = memo(() => {
	const { specification: { multiline } } = useNodeDOMWidgetContext<string, z.infer<typeof zStringInputOptions>>();

	return multiline
		? <StringTextareaField />
		: <StringTextField />;
});

const StringTextField = memo(() => {
	return <Suspense fallback={<StringTextFieldSkeleton />}>
		<Field>
			<StringFieldLabel />
			<StringTextFieldControl />
		</Field>
	</Suspense>;
});

const StringTextFieldSkeleton = memo(() => {
	return <FieldSkeleton>
		<FieldLabelSkeleton />
		<InputSkeleton />
	</FieldSkeleton>;
});

const StringTextareaField = memo(() => {
	return <Suspense fallback={<StringTextareaFieldSkeleton />}>
		<Field>
			<StringFieldLabel />
			<StringTextareaFieldControl />
		</Field>
	</Suspense>;
});

const StringTextareaFieldSkeleton = memo(() => {
	return <FieldSkeleton>
		<FieldLabelSkeleton />
		<TextareaSkeleton />
	</FieldSkeleton>;
});

const StringFieldLabel = memo(() => {
	const t = useNodeInputTranslation();
	const { specification } = useNodeDOMWidgetContext<string, z.infer<typeof zStringInputOptions>>();

	return <FieldLabel>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const StringTextFieldControl = memo(() => {
	const { specification } = useNodeDOMWidgetContext<string, z.infer<typeof zStringInputOptions>>();
	const value = useNodeDOMWidgetValue<string>();
	const on_value_change = useNodeDOMWidgetOnValueChange<string>();

	return <Input
		onValueChange={on_value_change}
		placeholder={specification.placeholder}
		value={value}
	/>;
});

const StringTextareaFieldControl = memo(() => {
	const { specification } = useNodeDOMWidgetContext<string, z.infer<typeof zStringInputOptions>>();
	const value = useNodeDOMWidgetValue<string>();
	const on_value_change = useNodeDOMWidgetOnValueChange<string>();

	return <Textarea
		onValueChange={on_value_change}
		placeholder={specification.placeholder}
		value={value}
	/>;
});
