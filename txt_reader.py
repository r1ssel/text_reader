import tkinter as tk
from tkinter import ttk

class InterfaceBuilder:
    def __init__(self, master):
        self.master = master
        self.master.title("Интерфейсный Конструктор")
        self.master.geometry("600x400")

        self.widgets_frame = ttk.Frame(self.master)
        self.widgets_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.canvas_frame = ttk.Frame(self.master)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Создаем виджеты для добавления
        ttk.Label(self.widgets_frame, text="Выберите виджет:").pack(pady=5)

        self.widget_type = tk.StringVar()
        self.widget_type.set("Label")

        widget_options = ["Label", "Button", "Entry"]
        widget_menu = ttk.OptionMenu(self.widgets_frame, self.widget_type, *widget_options)
        widget_menu.pack(pady=5)

        ttk.Label(self.widgets_frame, text="Текст:").pack(pady=5)
        self.widget_text = tk.Entry(self.widgets_frame)
        self.widget_text.pack(pady=5)

        ttk.Button(self.widgets_frame, text="Добавить", command=self.add_widget).pack(pady=10)

    def add_widget(self):
        widget_type = self.widget_type.get()
        text = self.widget_text.get()

        if widget_type == "Label":
            label = ttk.Label(self.canvas, text=text)
            label.pack(pady=5)
        elif widget_type == "Button":
            button = ttk.Button(self.canvas, text=text)
            button.pack(pady=5)
        elif widget_type == "Entry":
            entry = ttk.Entry(self.canvas)
            entry.pack(pady=5)

        self.widget_text.delete(0, tk.END)  # Очистить текстовое поле

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBuilder(root)
    root.mainloop()
