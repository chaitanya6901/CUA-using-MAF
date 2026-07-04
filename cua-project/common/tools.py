from pywinauto import Desktop
from pywinauto.keyboard import send_keys
from pywinauto.findwindows import find_elements
import subprocess
import time
import os
import pyperclip
import threading

_NP_HANDLE = None
_LOCK = threading.Lock()
_LAST_TEXT = ""

def _clean_session():
    pk = "%LOCALAPPDATA%\\Packages\\Microsoft.WindowsNotepad_8wekyb3d8bbwe\\LocalState"
    for sub in ("TabState", "WindowState"):
        d = os.path.expandvars(f"{pk}\\{sub}")
        if os.path.isdir(d):
            for f in os.listdir(d):
                try:
                    os.remove(os.path.join(d, f))
                except Exception:
                    pass

def _ensure():
    global _NP_HANDLE
    if _NP_HANDLE is not None:
        try:
            w = Desktop(backend="uia").window(handle=_NP_HANDLE)
            if w.exists():
                return w
        except Exception:
            pass
    elems = find_elements(class_name="Notepad", top_level_only=True, backend="uia")
    if not elems:
        os.system("taskkill /f /im notepad.exe >nul 2>&1")
        _clean_session()
        subprocess.Popen("notepad.exe")
        time.sleep(2)
        elems = find_elements(class_name="Notepad", top_level_only=True, backend="uia")
        if not elems:
            raise RuntimeError("Notepad not found")
    _NP_HANDLE = elems[0].handle
    return Desktop(backend="uia").window(handle=_NP_HANDLE)

def _save_dlg():
    for _ in range(10):
        try:
            return _ensure().child_window(title="Save as")
        except Exception:
            pass
        for w in Desktop(backend="uia").windows():
            if w.class_name() == "#32770" and "Save" in w.window_text():
                desktop_handle = w.handle
                return Desktop(backend="uia").window(handle=desktop_handle)
        time.sleep(0.3)
    raise RuntimeError("Save As dialog not found")

def launch_app(path: str = "notepad.exe") -> str:
    """Launch Notepad. Returns window title."""
    with _LOCK:
        _ensure()
        w = _ensure()
        return w.window_text()

def set_text(window_title: str, text: str) -> str:
    """Replace Notepad content with the given text."""
    with _LOCK:
        global _LAST_TEXT
        w = _ensure()
        w.set_focus()
        time.sleep(0.2)
        send_keys("^a{BS}")
        pyperclip.copy(text)
        send_keys("^v")
        _LAST_TEXT = text
        return "set text"

def trigger_save(window_title: str = "") -> str:
    """Send Ctrl+Shift+S to Notepad to open the Save As dialog (Win11)."""
    with _LOCK:
        w = _ensure()
        w.set_focus()
        global _LAST_TEXT
        if _LAST_TEXT:
            send_keys("^a{BS}")
            pyperclip.copy(_LAST_TEXT)
            send_keys("^v")
        send_keys("^+s")
        time.sleep(0.5)
        return "save triggered"

def fill_save_dialog(filename: str) -> str:
    """Fill the filename in the Save As dialog and confirm."""
    with _LOCK:
        dlg = _save_dlg()
        time.sleep(0.3)
        send_keys("^a{BS}")
        pyperclip.copy(filename)
        send_keys("^v")
        time.sleep(0.3)
        dlg.child_window(title="Save", control_type="Button").click_input()
        time.sleep(0.5)
        for _ in range(5):
            confirm = None
            for cw in Desktop(backend="uia").windows():
                t = ""
                try:
                    t = cw.window_text()
                except Exception:
                    pass
                if "already exists" in t or "Confirm Save As" in t:
                    confirm = cw
                    break
            if confirm is not None:
                for child in confirm.descendants():
                    t = ""
                    try:
                        t = child.window_text()
                    except Exception:
                        pass
                    if t.lower() in ("yes", "replace"):
                        child.click_input()
                        time.sleep(0.3)
                        break
                break
            time.sleep(0.3)
        return f"saved as {filename}"

def close_window() -> str:
    """Close Notepad."""
    with _LOCK:
        os.system("taskkill /f /im notepad.exe >nul 2>&1")
        global _NP_HANDLE
        _NP_HANDLE = None
        return "closed Notepad"

def list_controls(dialog_name: str = "") -> str:
    """List UI controls in a window for debugging."""
    with _LOCK:
        w = _ensure()
        lines = []
        for ctrl in w.descendants():
            try:
                info = f"{ctrl.class_name()}: {ctrl.window_text()[:60]}"
                lines.append(info)
            except Exception:
                pass
        return "\n".join(lines[:50])
