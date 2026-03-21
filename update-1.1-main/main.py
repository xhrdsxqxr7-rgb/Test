import os

# Вывод текущей рабочей директории
print("Текущая рабочая директория:", os.getcwd())

# Продолжение твоего кода
import keyboard
import requests
import os
import tkinter as tk
from PIL import Image, ImageTk
import queue

url = "https://st2.depositphotos.com/1036149/10828/i/950/depositphotos_108287536-stock-photo-funny-cartoon-hippo.jpg"
filename = "image.jpg"

if not os.path.exists(filename):
    print("Скачиваю картинку...")
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)

# Создаем очередь команд для GUI из потока keyboard
command_queue = queue.Queue()

def open_image():
    # Просто кладём команду в очередь
    command_queue.put("open_image")

# Основное окно tkinter (скрытое)
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
    # Проверяем очередь через 100 мс
    root.after(100, process_queue)

def show_fullscreen_image():
    top = tk.Toplevel()
    top.attributes("-fullscreen", True)
    top.attributes("-topmost", True)
    img = Image.open(filename)
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(top, image=tk_img)
    label.image = tk_img
    label.pack(expand=True)
    top.bind("<Escape>", lambda e: top.destroy())

# Регистрируем горячую клавишу
keyboard.add_hotkey("shift", open_image)

def exit_program():
    print("Выключение программы...")
    os._exit(0)

def check_exit_combo():
    if keyboard.is_pressed("space") and keyboard.is_pressed("f") and keyboard.is_pressed("l"):
        exit_program()

    root.after(100, check_exit_combo)

# Запуск проверки комбинации
root.after(100, check_exit_combo)

# Запускаем проверку очереди и основной цикл tkinter
root.after(100, process_queue)
root.mainloop()