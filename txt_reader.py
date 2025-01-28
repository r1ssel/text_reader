import os
import re
import tkinter as tk
from tkinter import ttk, Canvas
from tkinter.ttk import Progressbar

def process_log_file(file_path):
    """Обрабатывает один файл и возвращает количество успешных запросов."""
    successful_requests = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Ищем строки с количеством успешных запросов
            match = re.search(r'Кол-во успешных запросов:\s*(\d+)', line)
            if match:
                successful_requests = int(match.group(1))
                print(f"Файл: {file_path} - Найдено успешных запросов: {successful_requests}")

    return successful_requests

def analyze_logs(directory):
    """Анализирует все лог-файлы в указанной директории."""
    total_files = 0
    total_requests = 0
    max_requests = 0
    min_requests = float('inf')
    min_requests_file = None  # Для хранения имени файла с минимальным количеством запросов
    max_requests_file = None  # Для хранения имени файла с максимальным количеством запросов

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # Предполагаем, что файлы имеют расширение .txt
            total_files += 1
            file_path = os.path.join(directory, filename)
            requests = process_log_file(file_path)

            total_requests += requests
            if requests > max_requests:
                max_requests = requests
                max_requests_file = filename
            if requests < min_requests:
                min_requests = requests
                min_requests_file = filename  # Сохраняем имя файла с минимальным количеством запросов

    # Вычисляем среднее количество запросов
    average_requests = total_requests / total_files if total_files > 0 else 0

    return total_files, total_requests, max_requests, max_requests_file, min_requests, average_requests, min_requests_file

def update_stats():
    """Обновляет статистику в интерфейсе."""
    directory_path = '300ms_logs'  # Укажите путь к директории с лог-файлами
    total_files, total_requests, max_requests, max_requests_file, min_requests, average_requests, min_requests_file = analyze_logs(directory_path)

    # Обновляем метки с информацией
    total_files_label.config(text="Количество обработанных файлов:")
    total_files_value.config(text=str(total_files))

    total_requests_label.config(text="Общее количество успешных запросов:")
    total_requests_value.config(text=str(total_requests))

    max_requests_label.config(text="Максимальное количество запросов:")
    max_requests_value.config(text=f"{max_requests} (в файле: {max_requests_file})")

    min_requests_label.config(text="Минимальное количество запросов:")
    min_requests_value.config(text=f"{min_requests if min_requests != float('inf') else 0} (в файле: {min_requests_file})")

    average_requests_label.config(text="Среднее количество запросов:")
    average_requests_value.config(text=f"{average_requests:.2f}")

    # Обновляем прогресс-бар
    progress = (total_requests / 12000) * 100  # Рассчитываем процент
    progress_bar['value'] = progress

    # Обновляем текстовое отображение прогресса
    progress_text.set(f"{total_requests} / 12000 ({progress:.1f}%)")

    # Запланировать обновление через 5 секунд
    root.after(5000, update_stats)

# Создаем главное окно
root = tk.Tk()
root.title("txt_reader")
root.geometry("720x250")
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # Устанавливаем фоновый цвет

# Создаем стиль для меток
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", foreground="#333")

# Создаем метки для отображения информации
total_files_label = ttk.Label(root, text="Количество обработанных файлов:")
total_files_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

total_files_value = ttk.Label(root, text="0")
total_files_value.grid(row=0, column=1, sticky="e", padx=10, pady=5)

total_requests_label = ttk.Label(root, text="Общее количество успешных запросов:")
total_requests_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

total_requests_value = ttk.Label(root, text="0")
total_requests_value.grid(row=1, column=1, sticky="e", padx=10, pady=5)

max_requests_label = ttk.Label(root, text="Максимальное количество запросов:")
max_requests_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

max_requests_value = ttk.Label(root, text="0")
max_requests_value.grid(row=2, column=1, sticky="e", padx=10, pady=5)

min_requests_label = ttk.Label(root, text="Минимальное количество запросов:")
min_requests_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

min_requests_value = ttk.Label(root, text="0")
min_requests_value.grid(row=3, column=1, sticky="e", padx=10, pady=5)

average_requests_label = ttk.Label(root, text="Среднее количество запросов:")
average_requests_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

average_requests_value = ttk.Label(root, text="0.00")
average_requests_value.grid(row=4, column=1, sticky="e", padx=10, pady=5)

# Создаем прогресс-бар и растягиваем его на всю ширину окна
progress_bar = Progressbar(root, length=700)  # Устанавливаем длину прогресс-бара
progress_bar.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

# Создаем метку для отображения текста прогресса
progress_text = tk.StringVar()
progress_label = ttk.Label(root, textvariable=progress_text, font=("Helvetica", 12), background="#f0f0f0")
progress_label.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

# Запускаем обновление статистики
update_stats()

# Запускаем главный цикл приложения
root.mainloop()
