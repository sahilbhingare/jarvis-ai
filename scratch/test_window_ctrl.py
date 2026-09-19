import psutil
import ctypes
import subprocess

def test_minimize():
    # Win + D
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0) # Left Windows key down
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0) # D key down
    ctypes.windll.user32.keybd_event(0x44, 0, 2, 0) # D key up
    ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0) # Left Windows key up
    return "Minimized"

def test_close_app(target):
    target = target.lower().strip()
    proc_map = {
        'notepad': ['notepad.exe'],
        'calculator': ['calculatorapp.exe', 'calculator.exe'],
        'chrome': ['chrome.exe'],
        'code': ['code.exe'],
        'spotify': ['spotify.exe']
    }
    targets = proc_map.get(target, [f"{target}.exe"])
    closed = 0
    for p in psutil.process_iter(['name']):
        try:
            if p.info['name'] and p.info['name'].lower() in targets:
                p.terminate()
                closed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return f"Closed {closed} processes for {target}"

print(test_close_app('nonexistent_app'))
