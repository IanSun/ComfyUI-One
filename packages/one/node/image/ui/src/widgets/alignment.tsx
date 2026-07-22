import type { FC } from "react";

import { clsx } from "clsx";
import { useEffect, useState } from "react";
import styles from "./alignment.module.css";

export const AlignmentWidget: FC<{
	label: string;
	onChange: (value: string) => void;
	options: string[];
	value: string;
}> = ({ label, onChange, options, value }) => {
	const [_value, set_value] = useState(value);

	useEffect(() => {
		onChange(_value);
	}, [onChange, _value]);

	return (
		<div className={clsx("rounded-sm", "pt-3", "bg-node-component-header-surface", styles.root)}>
			<div className={clsx("text-center", "text-node-component-slot-text")}>
				<span>{label}</span>
				<span className={clsx("ml-1", "text-muted-foreground")}>{`(${_value})`}</span>
			</div>
			<div className={clsx("grid", "grid-cols-3", "gap-2", "p-3")}>
				{options.map((value, index) => (
					<div
						className={clsx(
							"flex",
							"aspect-square",
							"rounded-sm",
							{ ring: _value === value },
							"bg-component-node-background",
							_value === value ? "text-component-node-foreground" : "text-muted-foreground",
							"place-content-center",
							"cursor-pointer",
						)}
						onClick={() => {
							set_value(value);
						}}
					>
						<svg className={clsx("block", "w-1/2")} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
							{
								[
									<path className={styles.icon} d="M17 17L7 7M7 7V17M7 7H17" />,
									<path className={styles.icon} d="M12 19V5M12 5L5 12M12 5L19 12" />,
									<path className={styles.icon} d="M7 17L17 7M17 7H7M17 7V17" />,
									<path className={styles.icon} d="M19 12H5M5 12L12 19M5 12L12 5" />,
									<circle className={styles.icon} cx="12" cy="12" r="1" />,
									<path className={styles.icon} d="M5 12H19M19 12L12 5M19 12L12 19" />,
									<path className={styles.icon} d="M17 7L7 17M7 17H17M7 17V7" />,
									<path className={styles.icon} d="M12 5V19M12 19L19 12M12 19L5 12" />,
									<path className={styles.icon} d="M7 7L17 17M17 17V7M17 17H7" />,
								][index]
							}
						</svg>
					</div>
				))}
			</div>
		</div>
	);
};
