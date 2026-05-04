
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# Файл для сохранения истории
HISTORY_FILE = "password_history.json"

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("400x500")

        # Переменные для настроек
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # 1. Элементы интерфейса
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Ползунок длины пароля
        ttk.Label(frame, text="Длина пароля:").pack(anchor=tk.W)
        self.length_slider = ttk.Scale(frame, from_=6, to=32, orient=tk.HORIZONTAL, variable=self.length_var)
        self.length_slider.pack(fill=tk.X, pady=5)
        ttk.Label(frame, textvariable=self.length_var).pack()

        # Чекбоксы символов
        ttk.Checkbutton(frame, text="Цифры (0-9)", variable=self.use_digits).pack(anchor=tk.W)
        ttk.Checkbutton(frame, text="Заглавные (A-Z)", variable=self.use_upper).pack(anchor=tk.W)
        ttk.Checkbutton(frame, text="Строчные (a-z)", variable=self.use_lower).pack(anchor=tk.W)
        ttk.Checkbutton(frame, text="Спецсимволы (@#$)", variable=self.use_special).pack(anchor=tk.W)

        # Кнопка генерации
        self.gen_button = ttk.Button(frame, text="Сгенерировать", command=self.generate_password)
        self.gen_button.pack(pady=10)

        # Поле вывода
        self.result_entry = ttk.Entry(frame, font=("Arial", 12))
        self.result_entry.pack(fill=tk.X, pady=5)

        # Таблица истории (Treeview)
        ttk.Label(frame, text="История:").pack(anchor=tk.W, pady=(10, 0))
        self.history_tree = ttk.Treeview(frame, columns=("password"), show="headings", height=5)
        self.history_tree.heading("password", text="Пароль")
        self.history_tree.column("password", width=300)
        self.history_tree.pack(fill=tk.BOTH, expand=True)

    def generate_password(self):
        # 4. Проверка корректности (длина)
        length = self.length_var.get()
        if length < 4:
            messagebox.showwarning("Ошибка", "Минимальная длина — 4")
            return

        # Формирование пула символов
        chars = ""
        if self.use_digits.get(): chars += string.digits
        if self.use_upper.get(): chars += string.ascii_uppercase
        if self.use_lower.get(): chars += string.ascii_lowercase
        if self.use_special.get(): chars += "!@#$%^&*()"

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов")
            return

        # 2. Использование random
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Вывод и сохранение
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        self.save_to_history(password)

    def save_to_history(self, password):
        # 3. Сохранение в JSON
        history = self.load_history_from_file()
        history.append(password)
        # Храним последние 10
        history = history[-10:] 
        
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)
        self.update_history_tree(history)

    def load_history_from_file(self):
        if not os.path.exists(HISTORY_FILE):
            return []
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []

    def load_history(self):
        history = self.load_history_from_file()
        self.update_history_tree(history)

    def update_history_tree(self, history):
        # Очистка и обновление таблицы
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        for pw in reversed(history):
            self.history_tree.insert("", tk.END, values=(pw,))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
