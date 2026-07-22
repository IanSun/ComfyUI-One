import type { DOMWidgetProps } from "../../internal/node";
import type { InputSpec } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, zFloatInputOptions, zIntInputOptions } from "@/schemas/nodeDefSchema";
import type { ComponentProps } from "react";
import type { z } from "zod";

import { useStore } from "@nanostores/react";
import { cn } from "cn";
import { Minus, Plus } from "lucide-react";
import { memo, Suspense, useCallback, useMemo } from "react";
import { FieldLabel, FieldLabelSkeleton, NumberField, NumberFieldSkeleton } from "../../components/field";
import { Group } from "../../components/group";
import { Input, InputSkeleton } from "../../components/input";
import {
	InputGroup,
	InputGroupAddon,
	InputGroupAddonSkeleton,
	InputGroupButton,
	InputGroupButtonSkeleton,
	InputGroupInput,
	InputGroupInputSkeleton,
	InputGroupSkeleton,
} from "../../components/input-group";
import { Slider, SliderSkeleton } from "../../components/slider";
import { useNodeInputTranslation } from "../hooks/i18n";

const useNumberProps = ({
	specification,
	store,
	widget,
}: Pick<DOMWidgetProps<number, z.infer<typeof zFloatInputOptions | typeof zIntInputOptions>>, "specification" | "store" | "widget">) => {
	const value = useStore(store);

	const {
		max,
		min,
		step = 1,
	} = specification;

	const formatOptions = useMemo<Intl.NumberFormatOptions>(() => {
		const fraction_digits = String(step).split(".", 2)[1]?.length ?? 0;

		return {
			maximumFractionDigits: fraction_digits,
			minimumFractionDigits: fraction_digits,
		};
	}, [step]);

	const onChange = useCallback((value: number) => {
		widget.value = value;
	}, [widget]);

	return {
		formatOptions,
		maxValue: max,
		minValue: min,
		onChange,
		step,
		value,
	};
};

export const Number = memo((props: DOMWidgetProps<number, z.infer<typeof zFloatInputOptions | typeof zIntInputOptions>>) => {
	const { specification } = props;

	return specification.max! >= specification.min!
		? <NumberSliderUI {...props} />
		: <NumberUI {...props} />;
});

const NumberFieldLabel = memo(({
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

const NumberFieldLabelSkeleton = memo(({
	className,
}: Pick<ComponentProps<typeof NumberFieldLabel>, "className">) => {
	return <FieldLabelSkeleton className={cn("flex h-6 items-center", className)} />;
});

const NumberSliderUI = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<number, z.infer<typeof zFloatInputOptions | typeof zIntInputOptions>>) => {
	const props = useNumberProps({
		specification,
		store,
		widget,
	});

	return <Suspense fallback={<NumberSliderUISkeleton />}>
		<Group className="my-2 flex flex-col gap-1 select-none cursor-auto">
			<NumberField
				className="flex-row gap-2"
				{...props}
			>
				<NumberFieldLabel
					className="flex-1"
					definition={definition}
					specification={specification}
				/>
				<Input className="w-24 max-w-2/5 text-center" />
			</NumberField>
			<Slider {...props} />
		</Group>
	</Suspense>;
});

const NumberSliderUISkeleton = memo(() => {
	return <div className="opacity-20">
		<div className="my-2 flex flex-col gap-1 select-none cursor-auto animate-pulse">
			<NumberFieldSkeleton className="flex-row gap-2">
				<NumberFieldLabelSkeleton className="flex-1"/>
				<InputSkeleton className="w-24 max-w-2/5 justify-center" />
			</NumberFieldSkeleton>
			<SliderSkeleton />
		</div>
	</div>;
});

const NumberUI = memo(({
	definition,
	specification,
	store,
	widget,
}: DOMWidgetProps<number, z.infer<typeof zFloatInputOptions | typeof zIntInputOptions>>) => {
	const props = useNumberProps({
		specification,
		store,
		widget,
	});

	return <Suspense fallback={<NumberUISkeleton />}>
		<NumberField
			className="my-2"
			{...props}
		>
			<NumberFieldLabel
				definition={definition}
				specification={specification}
			/>
			<InputGroup>
				<InputGroupInput className="text-center" />
				<InputGroupAddon>
					<InputGroupButton
						size="icon"
						slot="decrement"
					>
						<Minus />
					</InputGroupButton>
				</InputGroupAddon>
				<InputGroupAddon align="inline-end">
					<InputGroupButton
						size="icon"
						slot="increment"
					>
						<Plus />
					</InputGroupButton>
				</InputGroupAddon>
			</InputGroup>
		</NumberField>
	</Suspense>;
});

const NumberUISkeleton = memo(() => {
	return <div className="opacity-20">
		<NumberFieldSkeleton className="my-2 animate-pulse">
			<NumberFieldLabelSkeleton />
			<InputGroupSkeleton>
				<InputGroupInputSkeleton className="justify-center" />
				<InputGroupAddonSkeleton>
					<InputGroupButtonSkeleton size="icon">
						<Minus />
					</InputGroupButtonSkeleton>
				</InputGroupAddonSkeleton>
				<InputGroupAddonSkeleton align="inline-end">
					<InputGroupButtonSkeleton size="icon">
						<Plus />
					</InputGroupButtonSkeleton>
				</InputGroupAddonSkeleton>
			</InputGroupSkeleton>
		</NumberFieldSkeleton>
	</div>;
});
