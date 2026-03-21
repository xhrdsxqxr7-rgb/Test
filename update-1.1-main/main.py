import os
import sys
import keyboard
import requests
import tkinter as tk
from PIL import Image, ImageTk
import queue

# Принудительная рабочая директория
os.chdir(os.path.dirname(os.path.abspath(__file__)))

url = "https://st2.depositphotos.com/1036149/10828/i/950/depositphotos_108287536-stock-photo-funny-cartoon-hippo.jpg"
filename = "image.jpg"

# Скачивание картинки, если её нет
if not os.path.exists(filename):
    try:
        response = requests.get(url, timeout=10)
        with open(filename, "wb") as f:
            f.write(response.content)
    except:
        pass

command_queue = queue.Queue()

def open_image():
    command_queue.put("open_image")

root = tk.Tk()
root.withdraw()

def process_queue():
    try:
        while True:
            command = command_queue.get_nowait()
            if command == "open_image":
                show_fullscreen_image()
    except queue.Empty:
        pass
    root.after(100, process_queue)

def show_fullscreen_image():
    if not os.path.exists(filename): return
    top = tk.Toplevel()
    top.attributes("-fullscreen", True)
    top.attributes("-topmost", True)
    
    # Чтобы окно точно было поверх всех, даже игр
    top.focus_force() 
    
    img = Image.open(filename)
    # Авто-подбор размера под экран
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(top, image=tk_img)
    label.image = tk_img
    label.pack()
    
    top.bind("<Escape>", lambda e: top.destroy())

# Регистрация горячей клавиши
keyboard.add_hotkey("shift", open_image)

def exit_program():
    os._exit(0)

def check_exit_combo():
    # Ваша секретная комбинация для выхода
    if keyboard.is_pressed("space") and keyboard.is_pressed("f") and keyboard.is_pressed("l"):
        exit_program()
    root.after(100, check_exit_combo)

root.after(100, check_exit_combo)
root.after(100, process_queue)
root.mainloop()