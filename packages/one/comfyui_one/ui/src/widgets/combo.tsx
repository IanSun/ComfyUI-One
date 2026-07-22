import type { zComboInputOptions } from "@comfyorg/object-info-parser";
import type { ComponentProps } from "react";
import type { z } from "zod";

import { Combobox as ComboboxPrimitive } from "@base-ui/react";
import { memo, Suspense, useMemo } from "react";
import {
	Combobox,
	ComboboxContent,
	ComboboxInput,
	ComboboxInputSkeleton,
	ComboboxItem,
	ComboboxList,
	FieldLabel,
	FieldLabelSkeleton,
	FieldSkeleton,
} from "../components";
import {
	useNodeDOMWidgetContext,
	useNodeDOMWidgetOnValueChange,
	useNodeDOMWidgetValue,
	useNodeInputTranslation,
} from "../hooks";

export const Combo = memo(() => {
	return <Suspense fallback={<ComboSkeleton />}>
		<ComboField />
	</Suspense>;
});

const ComboSkeleton = memo(() => {
	return <FieldSkeleton>
		<FieldLabelSkeleton />
		<ComboboxInputSkeleton />
	</FieldSkeleton>;
});

const ComboField = memo(() => {
	const t = useNodeInputTranslation();
	const { specification: { options } } = useNodeDOMWidgetContext<number | string, z.infer<typeof zComboInputOptions>>();
	const value = useNodeDOMWidgetValue<number | string>();
	const on_value_change = useNodeDOMWidgetOnValueChange<number | string>();

	const items = useMemo(
		() => ComboboxPrimitive.createItems(options, {
			getLabel: (option) => t(`options.${option}`, { defaultValue: option }),
			getValue: (option) => option,
		}),
		[options, t],
	);

	return <Combobox
		items={items}
		onValueChange={on_value_change}
		value={value}
	>
		<ComboFieldLabel />
		<ComboboxInput />
		<ComboboxContent>
			<ComboboxList>
				{
					(option: number | string, index) =>
						<ComboItem
							index={index}
							key={option}
							value={option}
						/>
				}
			</ComboboxList>
		</ComboboxContent>
	</Combobox>;
});

const ComboFieldLabel = memo(() => {
	const t = useNodeInputTranslation();
	const { specification } = useNodeDOMWidgetContext<number | string, z.infer<typeof zComboInputOptions>>();

	return <FieldLabel>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const ComboItem = memo(({
	value,
	...props
}: ComponentProps<typeof ComboboxItem>) => {
	const t = useNodeInputTranslation();

	return <ComboboxItem
		value={value as number | string}
		{...props}
	>
		{t(`options.${value}`, { defaultValue: value })}
	</ComboboxItem>;
});
