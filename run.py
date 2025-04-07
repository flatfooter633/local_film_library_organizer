import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, image_names, Label
from logging import config, getLogger
from utils.logger import user_config
import aiohttp
import asyncio
from os import path
from config import SEARCH_BY_NAME_QUERY
from app.app import rename_files
from PIL import ImageTk, Image

async def main():
    # Ваш код здесь
    logger.info("Событие 'main' обработано")
    # Ввод пути к папке с фильмами
    main_path = path.normpath(folder_path.get())
    create_folder = str(create_folder_var.get())
    # Создание aiohttp-сессии
    async with aiohttp.ClientSession() as session:
        await rename_files(session, main_path, SEARCH_BY_NAME_QUERY, create_folder)

def update_log_window(text_widget, message):
    text_widget.insert(tk.END, message + '\n')
    text_widget.see(tk.END)

if __name__ == "__main__":
    # Настройка логирования с использованием конфигурации
    config.dictConfig(user_config)
    # Получение root логгера
    logger = getLogger()

    # Создание главного окна
    root = tk.Tk()
    root.title("Movie Renamer")
    root.geometry("1200x675")  # Set window size to 1200x630 pixels
    root.configure(bg="grey")  # Set background color to light blue

    # Загрузка фонового изображения
    img = Image.open('background.png')
    background_image = ImageTk.PhotoImage(img)
    # root.image = background_image  # Set background image

    # Add image
    label = Label(root, image=background_image)
    label.place(x=0, y=0)

    # Add text
    label2 = Label(root, text="Movie Renamer",
                   font=("Unispace", 32),
                   bg="yellow",  # Use default background color
                   borderwidth=0,  # Remove border
                   )

    label2.pack(pady=50)
    # устанавливаем тему "classic"
    ttk.Style().theme_use("vista")

    # ttk.Button(text="Click").pack(anchor=CENTER, expand=1)

    # Создание текстового поля для ввода пути к папке с фильмами
    folder_path = tk.StringVar()
    folder_entry = tk.Entry(root, textvariable=folder_path, font=("Unispace", 14), width=40, justify='left')
    folder_entry.pack(pady=30)  # Increase vertical padding

    # Создание кнопки для выбора папки с фильмами
    def select_folder():
        folder = filedialog.askdirectory()
        folder_path.set(folder)

    folder_button = tk.Button(root, text="Select Folder", font=("Unispace", 14), command=select_folder, width=40, background='yellow', justify='left', anchor='w')
    folder_button.pack(padx=30)  # Increase horizontal padding

    # Создание чекбокса для создания папок по жанрам
    create_folder_var = tk.IntVar()
    create_folder_check = tk.Checkbutton(root, text="Sort by Genres", font=("Unispace", 14), variable=create_folder_var, height=1, width=20, background='yellow', justify='left', anchor='w')
    create_folder_check.pack(pady=30)  # Increase vertical padding

    # Создание кнопки для запуска приложения
    def start_app():
        asyncio.run(main())

    start_button = tk.Button(root, text="Start", font=("Unispace", 24), command=start_app, width=20, background='green')
    start_button.pack(pady=10)  # Increase vertical padding

    # Create a text widget for logging
    log_text = tk.Text(root, height=10, width=50)
    log_text.pack(pady=10)


    # Запуск главного цикла tkinter
    root.mainloop()