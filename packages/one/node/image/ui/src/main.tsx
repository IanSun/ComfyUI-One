import { createRoot } from "react-dom/client";
import { AlignmentWidget } from "./widgets/alignment";
import { app } from "@/scripts/app";

app.registerExtension({
	name: "One.Node.OneImageCropByAlignment",
	nodeCreated: (node) => {
		if ("OneImageCropByAlignment" !== node.comfyClass) {
			return;
		}

		const { widgets } = node;
		if (!widgets) {
			return;
		}

		const index = widgets.findIndex((widget) => "combo" === widget.type && "alignment" === widget.name);
		const widget = widgets[index];
		if (!widget) {
			return;
		}
		const { label, name, options, value } = widget;
		node.removeWidget(widget);

		{
			const element = document.createElement("div");
			const widget = node.addDOMWidget("alignment", "ONE.ALIGNMENT", element, {
				getMinHeight: () => 0,
			});
			widget.serializeValue = () => {
				return widget.value;
			};
			node.removeWidget(widget);
			widgets.splice(index, 0, widget);

			const root = createRoot(element);
			widget.onRemove = () => {
				root.unmount();
			};
			const onChange = ((value) => {
				widget.serializeValue = () => value;

				return (v: string) => {
					value = v;
				};
			})(value as string);
			root.render(
				<AlignmentWidget
					label={label ?? name}
					onChange={onChange}
					options={options.values as string[]}
					value={value as string}
				/>,
			);
		}
	},
});
