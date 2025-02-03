import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font
import json

class InterfaceBuilder:
    def __init__(self, master):
        self.master = master
        self.master.title("Интерфейсный Конструктор")
        self.master.geometry("800x600")

        self.widgets_frame = ttk.Frame(self.master)
        self.widgets_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.canvas_frame = ttk.Frame(self.master)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

        self.current_widget = None
        self.offset_x = 0
        self.offset_y = 0
        self.widget_list = []

    def create_widgets(self):
        # Создаем виджеты для добавления
        ttk.Label(self.widgets_frame, text="Выберите виджет:").pack(pady=5)

        self.widget_type = tk.StringVar()
        self.widget_type.set("Label")

        widget_options = ["Label", "Button", "Entry", "Text"]
        widget_menu = ttk.OptionMenu(self.widgets_frame, self.widget_type, *widget_options)
        widget_menu.pack(pady=5)

        ttk.Label(self.widgets_frame, text="Текст:").pack(pady=5)
        self.widget_text = tk.Entry(self.widgets_frame)
        self.widget_text.pack(pady=5)

        ttk.Button(self.widgets_frame, text="Добавить", command=self.add_widget).pack(pady=10)
        ttk.Button(self.widgets_frame, text="Удалить", command=self.remove_widget).pack(pady=10)
        ttk.Button(self.widgets_frame, text="Сохранить", command=self.save_layout).pack(pady=10)
        ttk.Button(self.widgets_frame, text="Загрузить", command=self.load_layout).pack(pady=10)

        self.widget_listbox = tk.Listbox(self.widgets_frame)
        self.widget_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        # Кнопки для изменения шрифта
        ttk.Button(self.widgets_frame, text="Изменить шрифт", command=self.change_font).pack(pady=10)
        ttk.Button(self.widgets_frame, text="Копировать текст", command=self.copy_text).pack(pady=10)
        ttk.Button(self.widgets_frame, text="Вставить текст", command=self.paste_text).pack(pady=10)

    def add_widget(self):
        widget_type = self.widget_type.get()
        text = self.widget_text.get()

        if widget_type == "Label":
            widget = ttk.Label(self.canvas, text=text)
        elif widget_type == "Button":
            widget = ttk.Button(self.canvas, text=text)
        elif widget_type == "Entry":
            widget = ttk.Entry(self.canvas)
            widget.insert(0, text)  # Вставляем текст в поле ввода
        elif widget_type == "Text":
            widget = tk.Text(self.canvas, height=5, width=20)
            widget.insert(tk.END, text)  # Вставляем текст в текстовое поле

        widget.bind("<Button-1>", self.on_widget_click)
        widget.bind("<B1-Motion>", self.on_widget_drag)
        widget.bind("<Button-3>", self.show_context_menu)  # Правый клик для контекстного меню
        widget.place(x=50, y=50)  # Начальная позиция
        self.widget_list.append(widget)
        self.widget_listbox.insert(tk.END, f"{widget_type}: {text}")

        self.widget_text.delete(0, tk.END)  # Очистить текстовое поле

    def on_widget_click(self, event):
        self.current_widget = event.widget
        self.offset_x = event.x
        self.offset_y = event.y

    def on_widget_drag(self, event):
        if self.current_widget:
            x = event.x_root - self.offset_x
            y = event.y_root - self.offset_y
            self.current_widget.place(x=x, y=y)

    def show_context_menu(self, event):
        if self.current_widget:
            context_menu = tk.Menu(self.master, tearoff=0)
            context_menu.add_command(label="Изменить цвет", command=self.change_color)
            context_menu.add_command(label="Изменить размер", command=self.change_size)
            context_menu.post(event.x_root, event.y_root)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color and self.current_widget:
            self.current_widget.config(background=color)

    def change_size(self):
        size_window = tk.Toplevel(self.master)
        size_window.title("Изменить размер")
        size_window.geometry("200x150")

        ttk.Label(size_window, text="Ширина:").pack(pady=5)
        width_entry = tk.Entry(size_window)
        width_entry.pack(pady=5)

        ttk.Label(size_window, text="Высота:").pack(pady=5)
        height_entry = tk.Entry(size_window)
        height_entry.pack(pady=5)

        def apply_size():
            width = width_entry.get()
            height = height_entry.get()
            if self.current_widget and width.isdigit() and height.isdigit():
                self.current_widget.config(width=int(width), height=int(height))
                size_window.destroy()

        ttk.Button(size_window, text="Применить", command=apply_size).pack(pady=10)

    def remove_widget(self):
        if self.current_widget:
            self.current_widget.destroy()
            self.widget_list.remove(self.current_widget)
            self.widget_listbox.delete(self.widget_listbox.curselection())
            self.current_widget = None

    def save_layout(self):
        layout = []
        for widget in self.widget_list:
            widget_info = {
                "type": widget.winfo_class(),
                "text": widget.get("text", ""),
                "x": widget.winfo_x(),
                "y": widget.winfo_y(),
                "bg": widget.cget("background"),
                "width": widget.winfo_width(),
                "height": widget.winfo_height()
            }
            layout.append(widget_info)

        with open("layout.json", "w") as f:
            json.dump(layout, f)
        messagebox.showinfo("Сохранение", "Верстка успешно сохранена!")

    def load_layout(self):
        try:
            with open("layout.json", "r") as f:
                layout = json.load(f)
            self.clear_canvas()
            for widget_info in layout:
                widget_type = widget_info["type"]
                text = widget_info["text"]
                x = widget_info["x"]
                y = widget_info["y"]
                bg = widget_info["bg"]
                width = widget_info["width"]
                height = widget_info["height"]

                if widget_type == "Label":
                    widget = ttk.Label(self.canvas, text=text, background=bg)
                elif widget_type == "Button":
                    widget = ttk.Button(self.canvas, text=text, background=bg)
                elif widget_type == "Entry":
                    widget = ttk.Entry(self.canvas, background=bg)
                    widget.insert(0, text)  # Вставляем текст в поле ввода
                elif widget_type == "Text":
                    widget = tk.Text(self.canvas, height=5, width=20, background=bg)
                    widget.insert(tk.END, text)  # Вставляем текст в текстовое поле

                widget.bind("<Button-1>", self.on_widget_click)
                widget.bind("<B1-Motion>", self.on_widget_drag)
                widget.place(x=x, y=y, width=width, height=height)
                self.widget_list.append(widget)
                self.widget_listbox.insert(tk.END, f"{widget_type}: {text}")
            messagebox.showinfo("Загрузка", "Верстка успешно загружена!")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл верстки не найден.")

    def clear_canvas(self):
        for widget in self.widget_list:
            widget.destroy()
        self.widget_list.clear()
        self.widget_listbox.delete(0, tk.END)

    def change_font(self):
        if self.current_widget:
            font_window = tk.Toplevel(self.master)
            font_window.title("Изменить шрифт")
            font_window.geometry("300x200")

            ttk.Label(font_window, text="Шрифт:").pack(pady=5)
            font_family = tk.StringVar(value="Arial")
            font_size = tk.StringVar(value="10")

            font_family_entry = ttk.Entry(font_window, textvariable=font_family)
            font_family_entry.pack(pady=5)

            ttk.Label(font_window, text="Размер:").pack(pady=5)
            font_size_entry = ttk.Entry(font_window, textvariable=font_size)
            font_size_entry.pack(pady=5)

            def apply_font():
                family = font_family.get()
                size = font_size.get()
                if family and size.isdigit():
                    new_font = (family, int(size))
                    self.current_widget.config(font=new_font)
                    font_window.destroy()

            ttk.Button(font_window, text="Применить", command=apply_font).pack(pady=10)

    def copy_text(self):
        if isinstance(self.current_widget, tk.Text):
            try:
                self.master.clipboard_clear()
                text = self.current_widget.get("1.0", tk.END)
                self.master.clipboard_append(text)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось скопировать текст: {e}")

    def paste_text(self):
        if isinstance(self.current_widget, tk.Text):
            try:
                text = self.master.clipboard_get()
                self.current_widget.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось вставить текст: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBuilder(root)
    root.mainloop()
