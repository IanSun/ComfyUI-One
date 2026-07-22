import type { PluginOption, UserConfig } from "vite";

import { randomUUIDv7 } from "node:crypto";
import { dirname, relative, resolve } from "node:path";
import { env } from "node:process";
import optimizeLocales from "@react-aria/optimize-locales-plugin";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import MagicString from "magic-string";
import { analyzer } from "vite-bundle-analyzer";

const config: UserConfig = {
	build: {
		minify: "oxc",
		modulePreload: {
			polyfill: false,
		},
		rolldownOptions: {
			external: ["@/scripts/app"],
			optimization: {
				inlineConst: {
					mode: "smart",
					pass: 3,
				},
			},
			output: {
				assetFileNames: "assets/[hash][extname]",
				chunkFileNames: "chunks/[hash].js",
				codeSplitting: {
					groups: [
						{
							name: "vendor-react",
							test: (id) => [
								"/node_modules/react/",
								"/node_modules/react-dom/",
							].some((part) => id.includes(part)),
						},
						{
							name: "vendor-i18next",
							test: (id) => [
								"/node_modules/i18next/",
								"/node_modules/i18next-http-backend/",
								"/node_modules/i18next-multiload-backend-adapter/",
								"/node_modules/react-i18next/",
							].some((part) => id.includes(part)),
						},
						{
							name: "vendor-aria",
							test: (id) => [
								"/node_modules/@react-aria/",
								"/node_modules/react-aria/",
								"/node_modules/react-aria-components/",
							].some((part) => id.includes(part)),
						},
						{
							name: "vendor",
							test: (id) => id.includes("/node_modules/"),
						},
					],
				},
				entryFileNames: "[name].js",
				hashCharacters: "hex",
				minify: {
					codegen: {
						removeWhitespace: true,
					},
				},
				paths: {
					"@/scripts/app": "../../scripts/app.js",
				},
			},
		},
		sourcemap: true,
		target: "esnext",
	},
	define: {
		"process.env.NODE_ENV": JSON.stringify("production"),
	},
	input: "src/main.ts",
	plugins: [
		analyzer({
			enabled: "build:inspect" === env.npm_lifecycle_event,
		}),
		css(),
		react(),
		tailwindcss(),
		optimizeLocales.vite({
			locales: ["en-US", "zh-CN"],
		}),
	],
};

function css(): PluginOption {
	const VIRTUAL_CSS_IMPORTER_MODULE_ID = "virtual:css/importer";
	const VIRTUAL_CSS_INTERNAL_MODULE_ID = "virtual:css/internal";

	const VIRTUAL_CSS_IMPORTER_MODULE_RESOLVED_ID = `\u{0}${VIRTUAL_CSS_IMPORTER_MODULE_ID}`;
	const VIRTUAL_CSS_IMPORTER_MODULE_RESOLVED_ID_PREFIX = `${VIRTUAL_CSS_IMPORTER_MODULE_RESOLVED_ID}#`;
	const VIRTUAL_CSS_IMPORTER_REFERENCE_FLAG = "VITE_PLUGIN_CSS_IMPORT_REFERENCE_FLAG";
	const VIRTUAL_CSS_IMPORTER_REFERENCE_LIST = "VITE_PLUGIN_CSS_IMPORT_REFERENCE_LIST";
	const VIRTUAL_CSS_INTERNAL_MODULE_RESOLVED_ID = `\u{0}${VIRTUAL_CSS_INTERNAL_MODULE_ID}`;

	const VIRTUAL_CSS_IMPORTER_MODULE_MAP = new Map<string, string>();

	return [
		{
			buildEnd: {
				handler() {
					VIRTUAL_CSS_IMPORTER_MODULE_MAP.clear();
				},
			},
			load: {
				handler(id) {
					if (!id.startsWith(VIRTUAL_CSS_IMPORTER_MODULE_RESOLVED_ID_PREFIX)) {
						return;
					}

					const reference_id = id.slice(VIRTUAL_CSS_IMPORTER_MODULE_RESOLVED_ID_PREFIX.length);
					const source = VIRTUAL_CSS_IMPORTER_MODULE_MAP.get(reference_id);
					if (!source) {
						return;
					}

					return `
						import { load } from "${VIRTUAL_CSS_INTERNAL_MODULE_ID}";
						export * from "${source}";

						if (${VIRTUAL_CSS_IMPORTER_REFERENCE_FLAG}) {
							load(${VIRTUAL_CSS_IMPORTER_REFERENCE_LIST}, import.meta.url);
						}
					`;
				},
			},
			name: "css:importer",
			resolveId: {
				order: "pre",
				async handler(source, importer) {
					if (!source.endsWith(".css") || importer?.startsWith(VIRTUAL_CSS_IMPORTER_MODULE_RESOLVED_ID_PREFIX)) {
						return;
					}

					const resolved = await this.resolve(source, importer);
					if (!resolved) {
						return;
					}

					const reference_id = randomUUIDv7().replaceAll("-", "");
					VIRTUAL_CSS_IMPORTER_MODULE_MAP.set(reference_id, resolved.id);

					return `${VIRTUAL_CSS_IMPORTER_MODULE_RESOLVED_ID_PREFIX}${reference_id}`;
				},
			},
		},
		{
			name: "css:injector",
			renderChunk: {
				order: "post",
				handler(code, chunk, options) {
					const { dir } = options;
					if (!dir) {
						return;
					}

					const s = new MagicString(code);

					if (chunk.viteMetadata?.importedCss.size) {
						const from = dirname(resolve(dir, chunk.fileName));

						s.replace(VIRTUAL_CSS_IMPORTER_REFERENCE_LIST, JSON.stringify(Array.from(chunk.viteMetadata.importedCss, (path) => relative(from, resolve(dir, path)))));
						s.replace(VIRTUAL_CSS_IMPORTER_REFERENCE_FLAG, ((flag = false) => {
							return () => JSON.stringify(!flag && (flag = true));
						})());
					}
					else {
						s.replaceAll(VIRTUAL_CSS_IMPORTER_REFERENCE_FLAG, JSON.stringify(false));
					}

					return {
						code: s.toString(),
						map: s.generateMap({ hires: "boundary" }),
					};
				},
			},
		},
		{
			load: {
				handler(id) {
					if (VIRTUAL_CSS_INTERNAL_MODULE_RESOLVED_ID === id) {
						return `
							export function load(sources, importer) {
								const fragment = new DocumentFragment();
								for (const source of sources) {
									const url = new URL(source, importer);
									const link = document.createElement("link");
									link.href = url.href;
									link.rel = "stylesheet";
									fragment.append(link);
								}
								document.head.append(fragment);
							};
						`;
					}
				},
			},
			name: "css:internal",
			resolveId: {
				async handler(source) {
					if (VIRTUAL_CSS_INTERNAL_MODULE_ID === source) {
						return VIRTUAL_CSS_INTERNAL_MODULE_RESOLVED_ID;
					}
				},
			},
		},
	];
}

export default config;
