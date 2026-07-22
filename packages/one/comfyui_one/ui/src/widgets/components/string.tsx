import type { DOMWidgetProps } from "../../internal/node";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, zStringInputOptions } from "@/schemas/nodeDefSchema";
import type { ComponentProps } from "react";
import type { z } from "zod";

import { useStore } from "@nanostores/react";
import { cn } from "cn";
import { memo, Suspense, useCallback } from "react";
import { FieldLabel, FieldLabelSkeleton, TextField, TextFieldSkeleton } from "../../components/field";
import { Input, InputSkeleton } from "../../components/input";
import { Textarea, TextareaSkeleton } from "../../components/textarea";
import { useNodeInputTranslation } from "../hooks/i18n";

const useStringProps = ({
	store,
	widget,
}: Pick<DOMWidgetProps<string, z.infer<typeof zStringInputOptions>>, "store" | "widget">) => {
	const value = useStore(store);

	const onChange = useCallback((value: string) => {
		widget.value = value;
	}, [widget]);

	return {
		onChange,
		value,
	};
};

export const String = memo((props: DOMWidgetProps<string, z.infer<typeof zStringInputOptions>>) => {
	const { specification } = props;

	return specification.multiline
		? <StringAreaUI {...props} />
		: <StringUI {...props} />;
});

const StringFieldLabel = memo(({
	className,
	definition,
	specification,
}: {
	definition: ComfyNodeDef;
	specification: InputSpec;
} & Pick<ComponentProps<typeof FieldLabel>, "className">) => {
	const t = useNodeInputTranslation(definition, specification);

	return <FieldLabel className={cn("flex h-6 items-center truncate text-node-component-slot-text", className)}>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const StringFieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof StringFieldLabel>, "className">) => {
	return <FieldLabelSkeleton className={cn("flex h-6 items-center", className)} />;
});

const StringAreaUI = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<string, z.infer<typeof zStringInputOptions>>) => {
	const props = useStringProps({
		store,
		widget,
	});

	return <Suspense fallback={<StringAreaUISkeleton />}>
		<TextField
			className="my-2"
			{...props}
		>
			<StringFieldLabel
				definition={definition}
				specification={specification}
			/>
			<Textarea />
		</TextField>
	</Suspense>;
});

const StringAreaUISkeleton = memo(() => {
	return <div className="opacity-20">
		<TextFieldSkeleton className="my-2 animate-pulse">
			<StringFieldLabelSkeleton />
			<TextareaSkeleton />
		</TextFieldSkeleton>
	</div>;
});

const StringUI = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<string, z.infer<typeof zStringInputOptions>>) => {
	const props = useStringProps({
		store,
		widget,
	});

	return <Suspense fallback={<StringUISkeleton />}>
		<TextField
			className="my-2"
			{...props}
		>
			<StringFieldLabel
				definition={definition}
				specification={specification}
			/>
			<Input />
		</TextField>
	</Suspense>;
});

const StringUISkeleton = memo(() => {
	return <div className="opacity-20">
		<TextFieldSkeleton className="my-2 animate-pulse">
			<StringFieldLabelSkeleton />
			<InputSkeleton />
		</TextFieldSkeleton>
	</div>;
});
