import os
import sys
import json
import requests
import tkinter as tk
from PIL import Image, ImageTk
from pynput import keyboard
import winreg

APP_NAME = "MyApp"
APP_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")
IMAGE_PATH = os.path.join(APP_DIR, "image.jpg")

DEFAULT_IMAGE_URL = "https://st2.depositphotos.com/1036149/10828/i/950/depositphotos_108287536-stock-photo-funny-cartoon-hippo.jpg"

def ensure_app_dir():
    os.makedirs(APP_DIR, exist_ok=True)

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "hotkey_show": "shift",
            "hotkey_exit": "alt+f8",
            "hotkey_settings": "alt+f9"
        }
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def download_image():
    if not os.path.exists(IMAGE_PATH):
        try:
            r = requests.get(DEFAULT_IMAGE_URL, timeout=10)
            with open(IMAGE_PATH, "wb") as f:
                f.write(r.content)
        except:
            pass

def add_to_startup():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except:
        pass

SPECIAL_KEYS = {
    "f1":  keyboard.Key.f1,
    "f2":  keyboard.Key.f2,
    "f3":  keyboard.Key.f3,
    "f4":  keyboard.Key.f4,
    "f5":  keyboard.Key.f5,
    "f6":  keyboard.Key.f6,
    "f7":  keyboard.Key.f7,
    "f8":  keyboard.Key.f8,
    "f9":  keyboard.Key.f9,
    "f10": keyboard.Key.f10,
    "f11": keyboard.Key.f11,
    "f12": keyboard.Key.f12,
    "insert": keyboard.Key.insert,
    "delete": keyboard.Key.delete,
    "home": keyboard.Key.home,
    "end": keyboard.Key.end,
    "space": keyboard.Key.space,
    "esc": keyboard.Key.esc,
}

MODIFIER_KEYS = {
    "shift": (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r),
    "ctrl":  (keyboard.Key.ctrl,  keyboard.Key.ctrl_l,  keyboard.Key.ctrl_r),
    "alt":   (keyboard.Key.alt,   keyboard.Key.alt_l,   keyboard.Key.alt_r),
}

def normalize_key(key):
    # Модификаторы
    for name, variants in MODIFIER_KEYS.items():
        if key in variants:
            return name
    # Специальные клавиши
    for name, k in SPECIAL_KEYS.items():
        if key == k:
            return name
    # Обычные символы — игнорируем (зависят от раскладки)
    return None

def parse_hotkey(hotkey_str):
    parts = [p.strip().lower() for p in hotkey_str.split("+")]
    return frozenset(parts)

class App:
    def __init__(self, settings):
        self.settings = settings
        self.root = tk.Tk()
        self.root.withdraw()

    def show_image(self):
        self.root.after(0, self._show_image_main_thread)

    def _show_image_main_thread(self):
        if not os.path.exists(IMAGE_PATH):
            return
        top = tk.Toplevel()
        top.attributes("-fullscreen", True)
        top.attributes("-topmost", True)
        img = Image.open(IMAGE_PATH)
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        img = img.resize((w, h), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=tk_img)
        label.image = tk_img
        label.pack()
        top.bind("<Escape>", lambda e: top.destroy())

    def open_settings(self):
        self.root.after(0, self._open_settings_main_thread)

    def _open_settings_main_thread(self):
        win = tk.Toplevel()
        win.title("Настройки")
        win.geometry("350x220")
        tk.Label(win, text="Показ (напр. alt+space):").pack()
        entry_show = tk.Entry(win)
        entry_show.insert(0, self.settings["hotkey_show"])
        entry_show.pack()
        tk.Label(win, text="Выход (напр. alt+f8):").pack()
        entry_exit = tk.Entry(win)
        entry_exit.insert(0, self.settings["hotkey_exit"])
        entry_exit.pack()
        tk.Label(win, text="Настройки (напр. alt+f9):").pack()
        entry_settings = tk.Entry(win)
        entry_settings.insert(0, self.settings["hotkey_settings"])
        entry_settings.pack()
        def save():
            self.settings["hotkey_show"] = entry_show.get()
            self.settings["hotkey_exit"] = entry_exit.get()
            self.settings["hotkey_settings"] = entry_settings.get()
            save_settings(self.settings)
            win.destroy()
        tk.Button(win, text="Сохранить", command=save).pack(pady=5)

    def exit_app(self):
        self.root.after(0, self._exit_main_thread)

    def _exit_main_thread(self):
        self.root.destroy()
        sys.exit(0)

class HotkeyListener:
    def __init__(self, app):
        self.app = app
        self.pressed = set()
        self._last_triggered = set()
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.daemon = True
        self.listener.start()

    def on_press(self, key):
        k = normalize_key(key)
        if k is None:
            return
        self.pressed.add(k)
        self._check()

    def on_release(self, key):
        k = normalize_key(key)
        if k:
            self.pressed.discard(k)
        self._last_triggered.clear()

    def _check(self):
        combos = {
            "show":     parse_hotkey(self.app.settings["hotkey_show"]),
            "exit":     parse_hotkey(self.app.settings["hotkey_exit"]),
            "settings": parse_hotkey(self.app.settings["hotkey_settings"]),
        }
        for name, combo in combos.items():
            if combo and combo.issubset(self.pressed) and name not in self._last_triggered:
                self._last_triggered.add(name)
                if name == "show":
                    self.app.show_image()
                elif name == "exit":
                    self.app.exit_app()
                elif name == "settings":
                    self.app.open_settings()

def main():
    ensure_app_dir()
    add_to_startup()
    download_image()
    settings = load_settings()
    app = App(settings)
    HotkeyListener(app)
    app.root.mainloop()

if __name__ == "__main__":
    main()