import type { DOMWidgetProps } from "../../internal/node";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, zComboInputOptions } from "@/schemas/nodeDefSchema";
import type { ComponentProps } from "react";
import type { z } from "zod";

import { memo, Suspense } from "react";
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
import { useValueProps } from "../hooks/component";
import { useNodeInputTranslation } from "../hooks/i18n";

export const Combo = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<number | string, z.infer<typeof zComboInputOptions>>) => {
	const { options } = specification;

	const props = useValueProps({
		store,
		widget,
	});

	return <Suspense fallback={<ComboSkeleton />}>
		<Field className="my-2">
			<ComboFieldLabel
				definition={definition}
				specification={specification}
			/>
			<Combobox
				defaultItems={options}
				{...props}
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

	return <FieldLabel className={className}>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const ComboFieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof ComboFieldLabel>, "className">) => {
	return <FieldLabelSkeleton className={className} />;
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
