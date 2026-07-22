import i18next from "i18next";
import Http from "i18next-http-backend";
import BackendAdapter from "i18next-multiload-backend-adapter";
import { initReactI18next } from "react-i18next";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Setting.Locale",
	beforeConfigureGraph: async (graph, missing, app) => {
		await i18next.changeLanguage(app.extensionManager.setting.get("Comfy.Locale"));
	},
	init: async () => {
		await i18next
			.use(BackendAdapter)
			.use(initReactI18next)
			.init({
				backend: {
					backend: Http,
					backendOption: {
						loadPath: "/api/i18n",
					},
				},
				fallbackLng: "en",
				interpolation: {
					escapeValue: false,
				},
			});
	},
});
