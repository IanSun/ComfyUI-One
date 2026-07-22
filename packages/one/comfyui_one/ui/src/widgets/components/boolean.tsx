import type { DOMWidgetProps } from "../../internal/node";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, zBooleanInputOptions } from "@/schemas/nodeDefSchema";
import type { ComponentProps } from "react";
import type { z } from "zod";

import { useStore } from "@nanostores/react";
import { cn } from "cn";
import { memo, Suspense, useCallback } from "react";
import { FieldLabel, FieldLabelSkeleton, SwitchField, SwitchFieldSkeleton } from "../../components/field";
import { Switch, SwitchSkeleton } from "../../components/switch";
import { useNodeInputTranslation } from "../hooks/i18n";

export const Boolean = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<boolean, z.infer<typeof zBooleanInputOptions>>) => {
	const value = useStore(store);

	const onChange = useCallback((value: boolean) => {
		widget.value = value;
	}, [widget]);

	return <Suspense fallback={<BooleanSkeleton />}>
		<SwitchField
			className="my-2"
			isSelected={value}
			onChange={onChange}
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

	return <FieldLabel className={cn("flex h-6 items-center truncate text-node-component-slot-text", className)}>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const BooleanFieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof BooleanFieldLabel>, "className">) => {
	return <FieldLabelSkeleton className={cn("flex h-6 items-center", className)} />;
});
