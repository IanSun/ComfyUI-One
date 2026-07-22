import type { UserConfig } from "vite";

import cssInjectedByJsPlugin from "vite-plugin-css-injected-by-js";

export default {
	build: {
		lib: {
			entry: {
				main: "src/main.ts",
			},
			formats: ["es"],
		},
		minify: "oxc",
		reportCompressedSize: false,
		rolldownOptions: {
			external: ["@/scripts/app"],
			optimization: {
				inlineConst: {
					mode: "smart",
					pass: 3,
				},
			},
			output: {
				minify: {
					codegen: {
						removeWhitespace: true,
					},
				},
				paths: {
					"@/scripts/app": "../../scripts/app.js",
				},
			},
			plugins: [
				{
					name: "comfyui",
					resolveId: (source) => {
						if ("../../scripts/app.js" === source) {
							return {
								external: true,
								id: "@/scripts/app",
							};
						}
					},
				},
			],
		},
		target: "esnext",
	},
	define: {
		"process.env.NODE_ENV": JSON.stringify("production"),
	},
	plugins: [cssInjectedByJsPlugin()],
} satisfies UserConfig;
