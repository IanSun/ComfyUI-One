import type { zBooleanInputOptions } from "@comfyorg/object-info-parser";
import type { z } from "zod";

import { memo, Suspense } from "react";
import {
	Field,
	FieldLabel,
	FieldLabelGroup,
	FieldLabelSkeleton,
	FieldSkeleton,
	Switch,
	SwitchSkeleton,
} from "../components";
import {
	useNodeDOMWidgetContext,
	useNodeDOMWidgetOnValueChange,
	useNodeDOMWidgetValue,
	useNodeInputTranslation,
} from "../hooks";

export const Boolean = memo(() => {
	return <Suspense fallback={<BooleanSkeleton />}>
		<Field>
			<FieldLabelGroup>
				<BooleanFieldLabel />
				<BooleanFieldControl />
			</FieldLabelGroup>
		</Field>
	</Suspense>;
});

const BooleanSkeleton = memo(() => {
	return <FieldSkeleton>
		<FieldLabelGroup>
			<FieldLabelSkeleton />
			<SwitchSkeleton />
		</FieldLabelGroup>
	</FieldSkeleton>;
});

const BooleanFieldLabel = memo(() => {
	const t = useNodeInputTranslation();
	const { specification } = useNodeDOMWidgetContext<boolean, z.infer<typeof zBooleanInputOptions>>();

	return <FieldLabel>
		{specification.display_name ?? t("name", { defaultValue: specification.name })}
	</FieldLabel>;
});

const BooleanFieldControl = memo(() => {
	const checked = useNodeDOMWidgetValue<boolean>();
	const on_checked_change = useNodeDOMWidgetOnValueChange<boolean>();

	return <Switch
		checked={checked}
		onCheckedChange={on_checked_change}
	/>;
});
