import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import stylistic from "@stylistic/eslint-plugin";
import { defineConfig, includeIgnoreFile } from "eslint/config";
import perfectionist from "eslint-plugin-perfectionist";
import { Alphabet } from "eslint-plugin-perfectionist/alphabet";
import unicorn from "eslint-plugin-unicorn";
import ts from "typescript-eslint";

export default defineConfig([
	includeIgnoreFile(fileURLToPath(new URL(".gitignore", import.meta.url)), {
		gitignoreResolution: true,
	}),
	{
		ignores: ["packages/@comfyorg"],
	},
	{
		extends: [
			js.configs.all,
			ts.configs.all,
			unicorn.configs.all,
			stylistic.configs.all,
			perfectionist.configs["recommended-alphabetical"],
		],
		files: ["**/*.{cjs,js,jsx,mjs,cts,mts,ts,tsx}"],
		languageOptions: { parserOptions: { projectService: true } },
		rules: {
			"@stylistic/array-element-newline": [
				"error",
				{
					consistent: true,
					multiline: true,
				},
			],
			"@stylistic/brace-style": ["error", "stroustrup"],
			"@stylistic/comma-dangle": ["error", "always-multiline"],
			"@stylistic/dot-location": ["error", "property"],
			"@stylistic/function-call-argument-newline": ["error", "consistent"],
			"@stylistic/function-paren-newline": ["error", "multiline-arguments"],
			"@stylistic/indent": ["error", "tab"],
			"@stylistic/indent-binary-ops": ["error", "tab"],
			"@stylistic/lines-around-comment": [
				"error",
				{
					allowBlockStart: true,
					allowObjectStart: true,
				},
			],
			"@stylistic/lines-between-class-members": ["error", "never"],
			"@stylistic/multiline-ternary": ["error", "always-multiline"],
			"@stylistic/object-curly-newline": [
				"error",
				{
					consistent: true,
					multiline: true,
				},
			],
			"@stylistic/object-curly-spacing": ["error", "always"],
			"@stylistic/operator-linebreak": ["error", "before"],
			"@stylistic/padded-blocks": ["error", "never"],
			"@stylistic/quote-props": ["error", "as-needed"],
			"@stylistic/space-before-function-paren": [
				"error",
				{
					anonymous: "always",
					asyncArrow: "always",
					catch: "always",
					named: "never",
				},
			],
			"@typescript-eslint/class-methods-use-this": "off",
			"@typescript-eslint/consistent-return": "off",
			"@typescript-eslint/explicit-function-return-type": [
				"error",
				{
					allowExpressions: true,
					allowFunctionsWithoutTypeParameters: true,
				},
			],
			"@typescript-eslint/max-params": "off",
			"@typescript-eslint/member-ordering": "off",
			"@typescript-eslint/naming-convention": "off",
			"@typescript-eslint/no-empty-function": ["error", { allow: ["arrowFunctions"] }],
			"@typescript-eslint/no-magic-numbers": "off",
			"@typescript-eslint/no-non-null-assertion": "off",
			"@typescript-eslint/no-shadow": "off",
			"@typescript-eslint/no-unsafe-member-access": "off",
			"@typescript-eslint/no-unsafe-return": "off",
			"@typescript-eslint/no-unsafe-type-assertion": "off",
			"@typescript-eslint/no-use-before-define": [
				"error",
				{
					functions: false,
					variables: false,
				},
			],
			"@typescript-eslint/non-nullable-type-assertion-style": "off",
			"@typescript-eslint/prefer-readonly-parameter-types": "off",
			"@typescript-eslint/promise-function-async": "off",
			"@typescript-eslint/require-await": "off",
			"@typescript-eslint/strict-boolean-expressions": [
				"error",
				{
					allowNullableBoolean: true,
					allowNullableEnum: true,
					allowNullableNumber: true,
					allowNullableString: true,
				},
			],
			"@typescript-eslint/switch-exhaustiveness-check": [
				"error",
				{
					considerDefaultExhaustiveForUnions: true,
				},
			],
			"arrow-body-style": "off",
			camelcase: "off",
			"func-style": [
				"error",
				"declaration",
				{
					allowArrowFunctions: true,
					allowTypeAnnotation: true,
				},
			],
			"id-length": "off",
			"max-depth": "off",
			"max-lines": "off",
			"max-lines-per-function": "off",
			"max-statements": "off",
			"no-duplicate-imports": ["error", { allowSeparateTypeImports: true }],
			"no-empty": ["error", { allowEmptyCatch: true }],
			"no-param-reassign": "off",
			"no-ternary": "off",
			"no-undefined": "off",
			"no-underscore-dangle": "off",
			"no-void": ["error", { allowAsStatement: true }],
			"one-var": "off",
			"perfectionist/sort-imports": [
				"error",
				{
					alphabet: Alphabet.generateRecommendedAlphabet()
						.sortByNaturalSort()
						.placeCharacterBefore({
							characterAfter: "-",
							characterBefore: "/",
						})
						.getCharacters(),
					groups: [
						"type-builtin",
						"type",
						{ newlinesBetween: 1 },
						"builtin",
						"external",
						"parent",
						"index",
						"sibling",
						"subpath",
						"style",
						"unknown",
					],
					newlinesBetween: "ignore",
					partitionByNewLine: false,
					type: "custom",
				},
			],
			"perfectionist/sort-objects": [
				"error",
				{
					groups: ["property", "method", "unknown"],
				},
			],
			"sort-imports": "off",
			"sort-keys": "off",
			"unicorn/consistent-arrow-return-style": "off",
			"unicorn/consistent-boolean-name": "off",
			"unicorn/consistent-function-scoping": "off",
			"unicorn/explicit-length-check": "off",
			"unicorn/filename-case": "off",
			"unicorn/max-nested-calls": "off",
			"unicorn/name-replacements": "off",
			"unicorn/no-array-callback-reference": "off",
			"unicorn/no-array-front-mutation": "off",
			"unicorn/no-array-reduce": "off",
			"unicorn/no-array-sort": "off",
			"unicorn/no-asterisk-prefix-in-documentation-comments": "off",
			"unicorn/no-await-expression-member": "off",
			"unicorn/no-barrel-files": "off",
			"unicorn/no-loop-iterable-mutation": "off",
			"unicorn/no-null": "off",
			"unicorn/no-unnecessary-splice": "off",
			"unicorn/no-unreadable-for-of-expression": "off",
			"unicorn/no-unreadable-object-destructuring": "off",
			"unicorn/no-unsafe-string-replacement": "off",
			"unicorn/prefer-continue": "off",
			"unicorn/prefer-global-this": "off",
			"unicorn/prefer-spread": "off",
			yoda: ["error", "always"],
		},
	},
	{
		files: ["**/*.{cjs,js,jsx,mjs}"],
		rules: { "@typescript-eslint/explicit-module-boundary-types": "off" },
	},
]);
