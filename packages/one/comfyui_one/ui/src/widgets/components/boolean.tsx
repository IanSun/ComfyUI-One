import type { DOMWidgetProps } from "../../internal/node";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, zBooleanInputOptions } from "@/schemas/nodeDefSchema";
import type { ComponentProps } from "react";
import type { z } from "zod";

import { memo, Suspense } from "react";
import { FieldLabel, FieldLabelSkeleton, SwitchField, SwitchFieldSkeleton } from "../../components/field";
import { Switch, SwitchSkeleton } from "../../components/switch";
import { useValueProps } from "../hooks/component";
import { useNodeInputTranslation } from "../hooks/i18n";

export const Boolean = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<boolean, z.infer<typeof zBooleanInputOptions>>) => {
	const props = useValueProps({
		store,
		widget,
	});

	return <Suspense fallback={<BooleanSkeleton />}>
		<SwitchField
			className="my-2"
			isSelected={props.value}
			onChange={props.onChange}
		>
			<BooleanFieldLabel
				className="flex-1"
				definition={definition}
				specification={specification}
			/>
			<Switch />
		</SwitchField>
	</Suspense>;
});

const BooleanSkeleton = memo(() => {
	return <div className="opacity-20">
		<SwitchFieldSkeleton className="my-2 animate-pulse">
			<BooleanFieldLabelSkeleton className="flex-1" />
			<SwitchSkeleton />
		</SwitchFieldSkeleton>
	</div>;
});

const BooleanFieldLabel = memo(({
	className,
	definition,
	specification,
}: {
	definition: ComfyNodeDef;
	specification: InputSpec;
} & Pick<ComponentProps<typeof FieldLabel>, "className">) => {
	const t = useNodeInputTranslation(definition, specification);

	return <FieldLabel className={className}>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const BooleanFieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof BooleanFieldLabel>, "className">) => {
	return <FieldLabelSkeleton className={className} />;
});
