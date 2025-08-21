"""
🖱️ Sophia Ghost in the Shell - Controller Module
STAGE 2: Embodied Movement - Human Input Emulation

This module provides a small, safe Controller API with optional fallbacks
when GUI automation libraries (pyautogui/keyboard) are not available.
It intentionally keeps side-effects minimal so it can be imported in tests
or headless CI environments without raising import errors.
"""

from typing import Tuple, List, Optional, Dict, Any
from datetime import datetime
import random
import time

# Try importing optional dependencies; provide lightweight stubs when missing
# Initialize flags once to avoid redefinition warnings from static checkers
pya_available: bool = False
key_available: bool = False

try:
    import pyautogui  # type: ignore
    pya_available = True
except Exception:
    # Lightweight, typed stub for headless environments
    class _PyAutoGuiStub:
        FAILSAFE: bool = True
        PAUSE: float = 0.0

        @staticmethod
        def size() -> Tuple[int, int]:
            return (1920, 1080)

        @staticmethod
        def position() -> Tuple[int, int]:
            return (0, 0)

        @staticmethod
        def moveTo(x: int, y: int, duration: float = 0.0, tween: Any = None) -> None:
            return None

        @staticmethod
        def click(*args: Any, **kwargs: Any) -> None:
            return None

        @staticmethod
        def mouseDown() -> None:
            return None

        @staticmethod
        def mouseUp() -> None:
            return None

        @staticmethod
        def scroll(amount: int) -> None:
            return None

        @staticmethod
        def typewrite(text: str, interval: float = 0.0) -> None:
            return None

    pyautogui = _PyAutoGuiStub()  # type: ignore

try:
    import keyboard  # type: ignore
    key_available = True
except Exception:
    class _KeyboardStub:
        @staticmethod
        def press_and_release(key: str) -> None:
            return None

        @staticmethod
        def send(combo: str) -> None:
            return None

    keyboard = _KeyboardStub()  # type: ignore


class Controller:
    """Minimal, safe controller abstraction for human-like input emulation."""

    def __init__(self, safety_enabled: bool = True):
        self.safety_enabled: bool = safety_enabled
        self.movement_log: List[Dict[str, Any]] = []
        self.last_action: Optional[Dict[str, Any]] = None

        # Try to configure GUI stubs safely
        try:
            if self.safety_enabled and hasattr(pyautogui, 'FAILSAFE'):
                pyautogui.FAILSAFE = True
                pyautogui.PAUSE = 0.05
        except Exception:
            pass

        try:
            self.screen_width, self.screen_height = pyautogui.size()
        except Exception:
            self.screen_width, self.screen_height = (1920, 1080)

    def human_like_delay(self, min_delay: float = 0.05, max_delay: float = 0.25) -> None:
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def natural_move_to(self, x: int, y: int, duration: Optional[float] = None) -> Dict[str, Any]:
        """Move the cursor with a best-effort human-like timing.

        This method is safe to call in headless environments because internal
        calls to pyautogui are wrapped in try/except blocks.
        """
        try:
            pos = pyautogui.position()
            try:
                current_x, current_y = int(pos.x), int(pos.y)  # type: ignore
            except Exception:
                current_x, current_y = int(pos[0]), int(pos[1])  # type: ignore
        except Exception:
            current_x, current_y = 0, 0

        if duration is None:
            distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
            duration = max(0.05, min(1.0, distance / 1000))

        final_x = max(0, min(self.screen_width - 1, x + random.randint(-2, 2)))
        final_y = max(0, min(self.screen_height - 1, y + random.randint(-2, 2)))

        try:
            tween = getattr(pyautogui, 'easeInOutQuad', None)
            if tween is not None:
                pyautogui.moveTo(final_x, final_y, duration=duration, tween=tween)
            else:
                pyautogui.moveTo(final_x, final_y, duration=duration)
        except Exception:
            # Running in a non-GUI environment; ignore
            pass

        self._log_action('move_mouse', {'from': [current_x, current_y], 'to': [final_x, final_y], 'duration': duration})

        return {'status': 'success', 'action': 'move_mouse', 'from': [current_x, current_y], 'to': [final_x, final_y], 'duration': duration}

    def smart_click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = 'left', clicks: int = 1) -> Dict[str, Any]:
        if x is not None and y is not None:
            move_result = self.natural_move_to(x, y)
            if move_result.get('status') == 'error':
                return move_result

            self.human_like_delay(0.06, 0.2)

        try:
            pos = pyautogui.position()
            try:
                pos_x, pos_y = int(pos.x), int(pos.y)  # type: ignore
            except Exception:
                pos_x, pos_y = int(pos[0]), int(pos[1])  # type: ignore
        except Exception:
            pos_x, pos_y = 0, 0

        try:
            if clicks == 1:
                pyautogui.click(button=button)
            else:
                pyautogui.click(clicks=clicks, interval=random.uniform(0.05, 0.15), button=button)
        except Exception:
            pass

        self._log_action('click', {'position': [pos_x, pos_y], 'button': button, 'clicks': clicks})

        return {'status': 'success', 'action': 'click', 'position': [pos_x, pos_y], 'button': button, 'clicks': clicks}

    def natural_type(self, text: str, typing_speed: float = 0.05) -> Dict[str, Any]:
        if not text:
            return {'status': 'error', 'action': 'type', 'error': 'No text provided'}

        for ch in text:
            delay = typing_speed + random.uniform(-0.02, 0.04)
            if ch.isupper() or ch in '.,!?;:':
                delay *= 1.3
            try:
                pyautogui.typewrite(ch, interval=max(0.01, delay))
            except Exception:
                # Ignore in headless/test environments
                pass

        self._log_action('type', {'text_preview': text[:60], 'length': len(text)})
        return {'status': 'success', 'action': 'type', 'text_length': len(text)}

    def press_key(self, key: str) -> Dict[str, Any]:
        self.human_like_delay(0.03, 0.12)
        try:
            keyboard.press_and_release(key)
        except Exception:
            pass
        self._log_action('press_key', {'key': key})
        return {'status': 'success', 'action': 'press_key', 'key': key}

    def hotkey_combination(self, *keys: str) -> Dict[str, Any]:
        combo = '+'.join(keys)
        self.human_like_delay(0.03, 0.12)
        try:
            keyboard.send(combo)
        except Exception:
            pass
        self._log_action('hotkey', {'combination': combo})
        return {'status': 'success', 'action': 'hotkey', 'combination': combo}

    def get_mouse_position(self) -> Dict[str, Any]:
        try:
            pos = pyautogui.position()
            try:
                x, y = int(pos.x), int(pos.y)  # type: ignore
            except Exception:
                x, y = int(pos[0]), int(pos[1])  # type: ignore
            return {'status': 'success', 'position': [x, y], 'screen_size': [self.screen_width, self.screen_height]}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def emergency_stop(self) -> None:
        try:
            pyautogui.moveTo(0, 0)
        except Exception:
            pass

    def _log_action(self, action_type: str, details: Dict[str, Any]) -> None:
        entry = {'timestamp': datetime.now().isoformat(), 'action': action_type, 'details': details}
        self.movement_log.append(entry)
        self.last_action = entry
        # keep last 200 actions
        if len(self.movement_log) > 200:
            self.movement_log = self.movement_log[-100:]


# Simple test when run directly
def test_controller() -> None:
    print('Testing Controller...')
    c = Controller()
    print(c.get_mouse_position())
    print(c.natural_move_to(100, 100))
    print(c.smart_click(100, 100))
    print(c.natural_type('Hello world'))


if __name__ == '__main__':
    test_controller()
