import type { InputSpec as InputSpecV2 } from "@/schemas/nodeDef/nodeDefSchemaV2";
import type { ComfyNodeDef, InputSpec as InputSpecV1 } from "@/schemas/nodeDefSchema";

export function transform_input_specification(
	name: string,
	specification: InputSpecV1,
	optional = false,
): InputSpecV2 {
	const options = {
		isOptional: optional,
		name,
		...specification[1],
	};

	const [type] = specification;

	if ("string" === typeof type) {
		return {
			type,
			...options,
		};
	}

	return {
		type: "UNKNOWN",
		...options,
	};
}

export function transform_input_specifications(input: ComfyNodeDef["input"]): InputSpecV2[] {
	return [input?.required, input?.optional].flatMap((record = {}, index) => {
		return Object.entries(record).map(([name, specification]) => {
			return transform_input_specification(name, specification, 1 === index);
		});
	});
}

export function transform_input_specifications_type<T extends ComfyNodeDef["input"]>(
	input: T,
	predicate: (specification: InputSpecV2) => boolean,
	callback: (specification: InputSpecV1) => void,
): T {
	for (const [index, record = {}] of [input?.required, input?.optional].entries()) {
		for (const [name, specification] of Object.entries(record)) {
			const s = transform_input_specification(name, specification, 1 === index);

			if (predicate(s)) {
				callback(specification);
			}
		}
	}

	return input;
}
