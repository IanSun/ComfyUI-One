import type { MouseEventHandler, PointerEventHandler, TouchEventHandler } from "react";

import { useCallback, useMemo } from "react";

export const useMouseEventListeners = (): {
	onMouseDown: MouseEventHandler;
} => {
	const mouse_event_cache = useMemo(() => new WeakSet<MouseEvent>(), []);

	const on_mouse_move = useCallback((event: MouseEvent) => {
		if (mouse_event_cache.has(event)) {
			return;
		}

		const { target } = event;
		if (!(target instanceof Node)) {
			return;
		}

		const { ownerDocument } = target;
		if (!ownerDocument) {
			return;
		}

		event.preventDefault();
		event.stopImmediatePropagation();

		event = new MouseEvent(event.type, event);
		mouse_event_cache.add(event);

		ownerDocument.dispatchEvent(event);
	}, [mouse_event_cache]);

	const on_mouse_up = useCallback((event: MouseEvent) => {
		const { target } = event;
		if (!(target instanceof Node)) {
			return;
		}

		const { ownerDocument } = target;
		if (!ownerDocument) {
			return;
		}

		event.preventDefault();
		event.stopImmediatePropagation();

		ownerDocument.removeEventListener("mousemove", on_mouse_move, { capture: true });
		ownerDocument.removeEventListener("mouseup", on_mouse_up, { capture: true });
		ownerDocument.dispatchEvent(new MouseEvent(event.type, event));
	}, [on_mouse_move]);

	const onMouseDown: MouseEventHandler = useCallback((event) => {
		const { target } = event;
		if (!(target instanceof Node)) {
			return;
		}

		const { ownerDocument } = target;
		if (!ownerDocument) {
			return;
		}

		event.stopPropagation();

		ownerDocument.addEventListener("mouseup", on_mouse_up, { capture: true });
		ownerDocument.addEventListener("mousemove", on_mouse_move, { capture: true });
	}, [on_mouse_move, on_mouse_up]);

	return {
		onMouseDown,
	};
};

export const usePointerEventListeners = (): {
	onPointerDown: PointerEventHandler;
} => {
	const pointer_event_cache = useMemo(() => new WeakSet<PointerEvent>(), []);
	const pointer_id_cache = useMemo(() => new Set<number>(), []);

	const on_pointer_move = useCallback((event: PointerEvent) => {
		if (pointer_event_cache.has(event) || !pointer_id_cache.has(event.pointerId)) {
			return;
		}

		const { target } = event;
		if (!(target instanceof Node)) {
			return;
		}

		const { ownerDocument } = target;
		if (!ownerDocument) {
			return;
		}

		event.preventDefault();
		event.stopImmediatePropagation();

		event = new PointerEvent(event.type, event);
		pointer_event_cache.add(event);

		ownerDocument.dispatchEvent(event);
	}, [pointer_event_cache, pointer_id_cache]);

	const on_pointer_cancel_or_up = useCallback((event: PointerEvent) => {
		if (!pointer_id_cache.has(event.pointerId)) {
			return;
		}

		const { target } = event;
		if (!(target instanceof Element)) {
			return;
		}

		event.preventDefault();
		event.stopImmediatePropagation();

		const { ownerDocument } = target;
		ownerDocument.removeEventListener("pointermove", on_pointer_move, { capture: true });
		ownerDocument.removeEventListener("pointercancel", on_pointer_cancel_or_up, { capture: true });
		ownerDocument.removeEventListener("pointerup", on_pointer_cancel_or_up, { capture: true });
		ownerDocument.dispatchEvent(new PointerEvent(event.type, event));

		pointer_id_cache.delete(event.pointerId);
	}, [on_pointer_move, pointer_id_cache]);

	const onPointerDown: PointerEventHandler = useCallback((event) => {
		const { target } = event;
		if (!(target instanceof Element)) {
			return;
		}

		event.stopPropagation();

		const { pointerId } = event;
		pointer_id_cache.add(pointerId);

		target.setPointerCapture(pointerId);

		const { ownerDocument } = target;
		ownerDocument.addEventListener("pointercancel", on_pointer_cancel_or_up, { capture: true });
		ownerDocument.addEventListener("pointerup", on_pointer_cancel_or_up, { capture: true });
		ownerDocument.addEventListener("pointermove", on_pointer_move, { capture: true });
	}, [on_pointer_move, on_pointer_cancel_or_up, pointer_id_cache]);

	return {
		onPointerDown,
	};
};

export const useTouchEventListeners = (): {
	onTouchStart: TouchEventHandler;
} => {
	const touch_event_cache = useMemo(() => new WeakSet<TouchEvent>(), []);
	const touch_id_cache = useMemo(() => new Set<number>(), []);

	const on_touch_move = useCallback((event: TouchEvent) => {
		if (touch_event_cache.has(event) || Array.from(event.touches).every((touch) => !touch_id_cache.has(touch.identifier))) {
			return;
		}

		const { target } = event;
		if (!(target instanceof Node)) {
			return;
		}

		const { ownerDocument } = target;
		if (!ownerDocument) {
			return;
		}

		event.preventDefault();
		event.stopImmediatePropagation();

		event = new TouchEvent(event.type, event as EventInit);
		touch_event_cache.add(event);

		ownerDocument.dispatchEvent(event);
	}, [touch_event_cache, touch_id_cache]);

	const on_touch_cancel_or_end = useCallback((event: TouchEvent) => {
		if (Array.from(event.touches).every((touch) => !touch_id_cache.has(touch.identifier))) {
			return;
		}

		const { target } = event;
		if (!(target instanceof Node)) {
			return;
		}

		const { ownerDocument } = target;
		if (!ownerDocument) {
			return;
		}

		event.preventDefault();
		event.stopImmediatePropagation();

		ownerDocument.removeEventListener("touchmove", on_touch_move, { capture: true });
		ownerDocument.removeEventListener("touchcancel", on_touch_cancel_or_end, { capture: true });
		ownerDocument.removeEventListener("touchend", on_touch_cancel_or_end, { capture: true });
		ownerDocument.dispatchEvent(new MouseEvent(event.type, event));

		for (const touch of Array.from(event.touches)) {
			touch_id_cache.delete(touch.identifier);
		}
	}, [on_touch_move, touch_id_cache]);

	const onTouchStart: TouchEventHandler = useCallback((event) => {
		const { target } = event;
		if (!(target instanceof Node)) {
			return;
		}

		const { ownerDocument } = target;
		if (!ownerDocument) {
			return;
		}

		event.stopPropagation();

		for (const touch of Array.from(event.touches)) {
			touch_id_cache.add(touch.identifier);
		}

		ownerDocument.addEventListener("touchcancel", on_touch_cancel_or_end, { capture: true });
		ownerDocument.addEventListener("touchend", on_touch_cancel_or_end, { capture: true });
		ownerDocument.addEventListener("touchmove", on_touch_move, { capture: true });
	}, [on_touch_move, on_touch_cancel_or_end, touch_id_cache]);

	return {
		onTouchStart,
	};
};
