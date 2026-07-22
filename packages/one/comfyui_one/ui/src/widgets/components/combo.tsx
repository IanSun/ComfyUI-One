import type { DOMWidgetProps } from "../../internal/node";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, zComboInputOptions } from "@/schemas/nodeDefSchema";
import type { ComponentProps } from "react";
import type { z } from "zod";

import { useStore } from "@nanostores/react";
import { cn } from "cn";
import { memo, Suspense, useCallback } from "react";
import {
	Combobox,
	ComboboxContent,
	ComboboxInput,
	ComboboxInputSkeleton,
	ComboboxItem,
	ComboboxList,
	ComboboxSkeleton,
} from "../../components/combobox";
import { Field, FieldLabel, FieldLabelSkeleton, FieldSkeleton } from "../../components/field";
import { useNodeInputTranslation } from "../hooks/i18n";

export const Combo = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<number | string, z.infer<typeof zComboInputOptions>>) => {
	const value = useStore(store);

	const { options } = specification;

	const onChange = useCallback((value: null | number | string) => {
		if (null !== value) {
			widget.value = value;
		}
	}, [widget]);

	return <Suspense fallback={<ComboSkeleton />}>
		<Field className="my-2">
			<ComboFieldLabel
				definition={definition}
				specification={specification}
			/>
			<Combobox
				defaultItems={options}
				onChange={onChange}
				value={value}
			>
				<ComboboxInput />
				<ComboboxContent>
					<ComboboxList>
						{options?.map(
							(option) =>
								<ComboItem
									definition={definition}
									id={option}
									key={option}
									specification={specification}
								/>,
						)}
					</ComboboxList>
				</ComboboxContent>
			</Combobox>
		</Field>
	</Suspense>;
});

const ComboSkeleton = memo(() => {
	return <div className="opacity-20">
		<FieldSkeleton className="my-2 animate-pulse">
			<ComboFieldLabelSkeleton />
			<ComboboxSkeleton>
				<ComboboxInputSkeleton />
			</ComboboxSkeleton>
		</FieldSkeleton>
	</div>;
});

const ComboFieldLabel = memo(({
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

const ComboFieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof ComboFieldLabel>, "className">) => {
	return <FieldLabelSkeleton className={cn("flex h-6 items-center", className)} />;
});

const ComboItem = memo(({
	definition,
	id,
	specification,
}: {
	definition: ComfyNodeDef;
	id: number | string;
	specification: InputSpec;
}) => {
	const t = useNodeInputTranslation(definition, specification);

	const value = t(`options.${id}`, { defaultValue: id });

	return <ComboboxItem id={id} key={id} textValue={value}>
		{value}
	</ComboboxItem>;
});
