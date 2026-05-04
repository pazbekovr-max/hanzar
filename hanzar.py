import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Класс для работы с данными (цитаты и история)
class QuoteManager:
    def __init__(self, filename="quotes_history.json"):
        self.filename = filename
        self.quotes = [
            {"text": "Счастье — это когда тебя понимают.", "author": "Высоцкий В.", "topic": "Счастье"},
            {"text": "Наука — это система познания, основанная на фактах.", "author": "Павлов И.П.", "topic": "Наука"},
            {"text": "Великие идеи приходят к тем, кто умеет ждать.", "author": "Толстой Л.Н.", "topic": "Мудрость"},
            {"text": "Код — это поэзия для машин.", "author": "Неизвестный", "topic": "Программирование"},
            {"text": "Россия — страна возможностей.", "author": "Официальная позиция", "topic": "Патриотизм"}
        ]
        self.history = []
        self.load_history()

    def get_random_quote(self):
        if not self.quotes:
            return None
        return random.choice(self.quotes)

    def add_to_history(self, quote):
        self.history.append(quote)
        self.save_history()

    def save_history(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                self.history = []

    def filter_quotes(self, author=None, topic=None):
        filtered = self.quotes
        if author:
            filtered = [q for q in filtered if author.lower() in q['author'].lower()]
        if topic:
            filtered = [q for q in filtered if topic.lower() in q['topic'].lower()]
        return filtered

    def add_new_quote(self, text, author, topic):
        if not text or not author or not topic:
            raise ValueError("Все поля (текст, автор, тема) должны быть заполнены.")
        new_quote = {"text": text, "author": author, "topic": topic}
        self.quotes.append(new_quote)
        return new_quote

# GUI Приложение
class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")
        
        self.manager = QuoteManager()

        # Верхняя панель: Генерация
        frame_top = tk.Frame(root, pady=20)
        frame_top.pack()

        self.lbl_quote = tk.Label(frame_top, text="Нажмите кнопку, чтобы получить цитату", wraplength=500, font=("Arial", 12), justify="center")
        self.lbl_quote.pack(pady=10)

        self.btn_generate = tk.Button(frame_top, text="Сгенерировать цитату", command=self.generate_quote, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_generate.pack(pady=5)

        # Панель фильтрации
        frame_filter = tk.Frame(root, pady=10)
        frame_filter.pack()

        tk.Label(frame_filter, text="Фильтр по автору:").grid(row=0, column=0, padx=5)
        self.entry_author = tk.Entry(frame_filter)
        self.entry_author.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Фильтр по теме:").grid(row=0, column=2, padx=5)
        self.entry_topic = tk.Entry(frame_filter)
        self.entry_topic.grid(row=0, column=3, padx=5)

        self.btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter)
        self.btn_filter.grid(row=0, column=4, padx=10)
        
        self.btn_reset_filter = tk.Button(frame_filter, text="Сброс", command=self.reset_filter)
        self.btn_reset_filter.grid(row=0, column=5, padx=5)

        # Панель добавления новой цитаты
        frame_add = tk.LabelFrame(root, text="Добавить новую цитату", padx=10, pady=10)
        frame_add.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_add, text="Текст:").grid(row=0, column=0, sticky="w")
        self.entry_new_text = tk.Entry(frame_add, width=30)
        self.entry_new_text.grid(row=0, column=1, padx=5)

        tk.Label(frame_add, text="Автор:").grid(row=1, column=0, sticky="w")
        self.entry_new_author = tk.Entry(frame_add, width=30)
        self.entry_new_author.grid(row=1, column=1, padx=5)

        tk.Label(frame_add, text="Тема:").grid(row=2, column=0, sticky="w")
        self.entry_new_topic = tk.Entry(frame_add, width=30)
        self.entry_new_topic.grid(row=2, column=1, padx=5)

        self.btn_add = tk.Button(frame_add, text="Добавить в базу", command=self.add_new_quote)
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # Панель истории
        frame_history = tk.LabelFrame(root, text="История сгенерированных цитат", padx=10, pady=10)
        frame_history.pack(fill="both", expand=True, padx=20, pady=10)

        self.listbox = tk.Listbox(frame_history, height=10, width=70)
        self.listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frame_history, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.update_history_list()

    def generate_quote(self):
        quote = self.manager.get_random_quote()
        if quote:
            display_text = f'"{quote["text"]}"\n— {quote["author"]} ({quote["topic"]})'
            self.lbl_quote.config(text=display_text)
            self.manager.add_to_history(quote)
            self.update_history_list()
        else:
            messagebox.showwarning("Внимание", "Список цитат пуст!")

    def apply_filter(self):
        author = self.entry_author.get()
        topic = self.entry_topic.get()
        quotes = self.manager.filter_quotes(author, topic)
        
        self.listbox.delete(0, tk.END)
        if not quotes:
            self.listbox.insert(tk.END, "Цитат не найдено по заданным фильтрам.")
        else:
            for q in quotes:
                self.listbox.insert(tk.END, f"{q['author']} ({q['topic']}): {q['text'][:40]}...")

    def reset_filter(self):
        self.entry_author.delete(0, tk.END)
        self.entry_topic.delete(0, tk.END)
        self.listbox.delete(0, tk.END)
        for q in self.manager.quotes:
            self.listbox.insert(tk.END, f"{q['author']} ({q['topic']}): {q['text'][:40]}...")

    def add_new_quote(self):
        text = self.entry_new_text.get()
        author = self.entry_new_author.get()
        topic = self.entry_new_topic.get()

        try:
            new_quote = self.manager.add_new_quote(text, author, topic)
            messagebox.showinfo("Успех", "Цитата успешно добавлена!")
            self.entry_new_text.delete(0, tk.END)
            self.entry_new_author.delete(0, tk.END)
            self.entry_new_topic.delete(0, tk.END)
            self.reset_filter() # Обновить список с новой цитатой
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def update_history_list(self):
        # Очищаем и заполняем историю (последние 10 записей для краткости в списке)
        self.listbox.delete(0, tk.END)
        for quote in reversed(self.manager.history[-10:]):
            self.listbox.insert(tk.END, f"История: {quote['author']} - {quote['text'][:30]}...")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
