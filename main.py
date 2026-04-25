import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from tkcalendar import DateEntry

# --- Конфигурация ---
DATA_FILE = "data/expenses.json"
DATE_FORMAT = "%Y-%m-%d"

# --- Логика работы с данными (Модель) ---

def load_data():
    """Загружает данные из JSON-файла. Возвращает пустой список, если файл не найден."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(data):
    """Сохраняет список расходов в JSON-файл."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def validate_input(amount_str, date_str):
    """Проверяет корректность введённых данных. Возвращает кортеж (is_valid, error_message)."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Сумма должна быть положительным числом."
    except ValueError:
        return False, "Введите корректное числовое значение для суммы."
    
    try:
        datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        return False, f"Дата должна быть в формате ГГГГ-ММ-ДД (например, 2026-04-25)."
    
    return True, ""

# --- Логика GUI (Контроллер) ---

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x500")
        
        self.expenses = load_data()
        
        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        # --- Рамка для добавления расхода ---
        frame_add = tk.LabelFrame(self.root, text="Добавить новый расход", padx=10, pady=10)
        frame_add.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Поля ввода
        tk.Label(frame_add, text="Сумма:").grid(row=0, column=0, sticky="e")
        self.amount_entry = tk.Entry(frame_add, width=15)
        self.amount_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(frame_add, text="Категория:").grid(row=1, column=0, sticky="e")
        self.category_entry = tk.Entry(frame_add, width=15)
        self.category_entry.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(frame_add, text="Дата:").grid(row=2, column=0, sticky="e")
        # Используем DateEntry для удобства выбора даты
        self.date_picker = DateEntry(frame_add, date_pattern=DATE_FORMAT.replace("%", ""))
        self.date_picker.grid(row=2, column=1, sticky="w", pady=5)

        # Кнопка добавления
        tk.Button(frame_add, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Таблица расходов ---
        columns = ("amount", "category", "date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        
        self.tree.column("amount", width=100, anchor="e")
        self.tree.column("category", width=250, anchor="w")
        self.tree.column("date", width=120, anchor="c")
        
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

        # --- Рамка для фильтрации ---
        frame_filter = tk.LabelFrame(self.root, text="Фильтр и поиск", padx=10, pady=10)
        frame_filter.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # Фильтр по категории
        tk.Label(frame_filter, text="Категория:").grid(row=0, column=0, sticky="e")
        self.filter_category_var = tk.StringVar()
        tk.Entry(frame_filter, textvariable=self.filter_category_var).grid(row=0, column=1, sticky="w", padx=5)

        # Фильтр по датам (используем DateEntry)
        tk.Label(frame_filter, text="Период с:").grid(row=1, column=0, sticky="e")
        self.filter_date_from = DateEntry(frame_filter, date_pattern=DATE_FORMAT.replace("%", ""))
        self.filter_date_from.grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(frame_filter, text="по:").grid(row=1, column=2, sticky="e")
        self.filter_date_to = DateEntry(frame_filter, date_pattern=DATE_FORMAT.replace("%", ""))
        self.filter_date_to.grid(row=1, column=3, sticky="w", padx=(5, 20))

        # Кнопка применения фильтра
        tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filters).grid(row=2, column=0, columnspan=4)

         # Метка для отображения итоговой суммы
        self.total_label = tk.Label(self.root, text="Итого: 0.00 ₽", font=("Arial", 12, "bold"))
        self.total_label.grid(row=3, column=0, sticky="w", padx=10)

    def add_expense(self):
        """Обработчик кнопки 'Добавить расход'."""
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        
         # Получаем дату в нужном формате из виджета DateEntry
         # .get_date() возвращает объект datetime.date -> форматируем в строку
         # .get() возвращает строку в формате dd.mm.yyyy -> преобразуем в ГГГГ-ММ-ДД
         # Здесь используем .get() и преобразование для совместимости с логикой валидации
         # Но лучше использовать .get_date() и форматировать её.
         # Для простоты примера оставим преобразование строки.
         # В реальном проекте лучше использовать .get_date().
         
         # Вариант 1 (через get_date):
         # date_obj = self.date_picker.get_date()
         # date_str = date_obj.strftime(DATE_FORMAT)
         
         # Вариант 2 (через get и преобразование):
         raw_date = self.date_picker.get()
         day, month, year = raw_date.split(".")
         date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
         
         is_valid, error_msg = validate_input(amount, date_str)
         
         if not is_valid:
             messagebox.showerror("Ошибка ввода", error_msg)
             return

         expense = {
             "amount": float(amount),
             "category": category,
             "date": date_str
         }
         
         self.expenses.append(expense)
         save_data(self.expenses)
         
         # Добавляем строку в таблицу и обновляем общую сумму
         self.tree.insert("", "end", values=(f"{float(amount):.2f}", category, date_str))
         self.update_total_label()
         
         # Очистка полей ввода
         self.amount_entry.delete(0, tk.END)
         self.category_entry.delete(0, tk.END)
         self.date_picker.set_date(datetime.now()) # Сброс даты на текущую

    def populate_treeview(self):
        """Заполняет таблицу всеми расходами из памяти при запуске."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for exp in self.expenses:
            self.tree.insert("", "end", values=(f"{exp['amount']:.2f}", exp['category'], exp['date']))
            
    def apply_filters(self):
        """Применяет фильтры по категории и дате к данным в таблице."""
        
        filter_cat = self.filter_category_var.get().lower()
        
         # Получаем даты из виджетов и форматируем их в ГГГГ-ММ-ДД
         # Аналогично add_expense:
         
         raw_from = self.filter_date_from.get()
         d_from, m_from, y_from = raw_from.split(".")
         filter_date_from = f"{y_from}-{m_from.zfill(2)}-{d_from.zfill(2)}" if raw_from else None

         raw_to = self.filter_date_to.get()
         d_to, m_to, y_to = raw_to.split(".")
         filter_date_to = f"{y_to}-{m_to.zfill(2)}-{d_to.zfill(2)}" if raw_to else None

         filtered_expenses = []
         
         for exp in self.expenses:
             match_category = True if not filter_cat else filter_cat in exp['category'].lower()
             match_date_from = True if not filter_date_from else exp['date'] >= filter_date_from
             match_date_to   = True if not filter_date_to   else exp['date'] <= filter_date_to

             if match_category and match_date_from and match_date_to:
                 filtered_expenses.append(exp)
                 
                 # Вставляем в таблицу (Treeview очищается перед этим в методе ниже)
                 # Здесь мы только собираем данные для подсчета суммы.
                 # Вставку в таблицу лучше делать один раз после цикла.
                 
         # Очищаем таблицу перед вставкой новых данных
         for item in self.tree.get_children():
             self.tree.delete(item)
             
         total_sum = 0.0
         
         for exp in filtered_expenses:
             total_sum += exp['amount']
             self.tree.insert("", "end", values=(f"{exp['amount']:.2f}", exp['category'], exp['date']))
                         
         
                   
         
         
         


    def update_total_label(self):
       """Обновляет метку с общей суммой всех видимых расходов."""
       total_sum = sum(float(item[0].replace(',', '.')) for item in self.tree.get_children())
       self.total_label.config(text=f"Итого: {total_sum:.2f} ₽")


# --- Точка входа в программу ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    
    # Настройка весов для сетки (чтобы элементы растягивались при изменении окна)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    root.mainloop()
