export function serialize<
	T extends ((...args: any[]) => Promise<void> | void),
>(...callbacks: (T | undefined)[]): T {
	return new Proxy<T>((() => {}) as T, {
		apply: async (_, thisArg, args) => {
			for (const callback of callbacks) {
				if (callback) {
					await Reflect.apply(callback, thisArg, args);
				}
			}
		},
	});
}
