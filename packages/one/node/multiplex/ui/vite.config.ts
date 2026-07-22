import type { UserConfig } from "vite";

import dts from "unplugin-dts/vite";

export default {
	build: {
		lib: {
			entry: {
				main: "src/main.ts",
			},
			formats: ["es"],
		},
		minify: false,
		reportCompressedSize: false,
		rolldownOptions: {
			external: ["@one/shared", "@/scripts/app"],
			output: {
				paths: {
					"@/scripts/app": "../../scripts/app.js",
				},
			},
		},
		target: "esnext",
	},
	plugins: [
		dts({
			aliasesExclude: [/@\/.+/u],
			bundleTypes: true,
			tsconfigPath: "tsconfig.ui.json",
		}),
	],
} satisfies UserConfig;
