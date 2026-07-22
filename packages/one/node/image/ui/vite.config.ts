import type { UserConfig } from "vite";

import react from "@vitejs/plugin-react";
import { libInjectCss } from "vite-plugin-lib-inject-css";

export default {
	build: {
		cssCodeSplit: true,
		lib: {
			entry: {
				main: "src/main.tsx",
			},
			formats: ["es"],
		},
		minify: false,
		reportCompressedSize: false,
		rolldownOptions: {
			external: ["clsx", "react", "react/jsx-runtime", "react-dom/client", "@/scripts/app"],
			output: {
				paths: {
					"@/scripts/app": "../../scripts/app.js",
				},
			},
		},
		target: "esnext",
	},
	css: {
		modules: {
			generateScopedName: "[contenthash:base52:1][contenthash:base64safe:5]",
		},
	},
	plugins: [libInjectCss(), react()],
} satisfies UserConfig;
