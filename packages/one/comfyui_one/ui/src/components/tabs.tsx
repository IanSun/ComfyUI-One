import type { ComponentProps } from "react";

import { cn } from "cn";
import { memo } from "react";
import {
	TabList as TabListPrimitive,
	TabPanel as TabPanelPrimitive,
	Tab as TabPrimitive,
	Tabs as TabsPrimitive,
} from "react-aria-components";

export const Tabs = memo(({
	className,
	...props
}: ComponentProps<typeof TabsPrimitive>) => {
	return <TabsPrimitive
		className={cn(
			"group/tabs flex flex-col gap-2",
			className,
		)}
		data-slot="tabs"
		{...props}
	/>;
});

export const TabsContent = memo(({
	className,
	...props
}: ComponentProps<typeof TabPanelPrimitive>) => {
	return (
		<TabPanelPrimitive
			className={cn("flex-1", className)}
			data-slot="tabs-content"
			{...props}
		/>
	);
});

export const TabsList = memo(({
	className,
	...props
}: ComponentProps<typeof TabListPrimitive>) => {
	return (
		<TabListPrimitive
			className={cn(
				"group/tabs-list inline-flex w-fit h-6 rounded-md bg-component-node-widget-background items-center justify-center",
				className,
			)}
			data-slot="tabs-list"
			{...props}
		/>
	);
});

export const TabsTrigger = memo(({
	className,
	...props
}: ComponentProps<typeof TabPrimitive>) => {
	return (
		<TabPrimitive
			className={cn(
				"flex-1 inline-flex h-full rounded-md bg-component-node-widget-background-selected/0 selected:bg-component-node-widget-background-selected items-center justify-center px-1.5 py-0.5 text-component-node-foreground/70 selected:text-component-node-foreground text-xs text-center truncate shadow-none selected:shadow-sm transition-[background-color,box-shadow,color] cursor-default",
				className,
			)}
			data-slot="tabs-trigger"
			{...props}
		/>
	);
});
