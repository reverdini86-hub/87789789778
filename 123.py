ᴋɪʀᴀ, [26.11.2025 19: 56]
import tkinter as tk
from tkinter import messagebox
import sqlite3


class SimpleMedicalApp:
    def init(self):
        self.root = tk.Tk()
        self.root.title("Медсправочник")
        self.root.geometry("400x300")

        self.create_db()
        self.show_login()

    def create_db(self):
        conn = sqlite3.connect("medical.db")
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                login TEXT,
                password TEXT,
                role TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT
            )
        """)

        # Добавляем тестового админа
        cur.execute("SELECT * FROM users WHERE login='admin'")
        if not cur.fetchone():
            cur.execute("INSERT INTO users (login, password, role) VALUES ('admin', 'admin', 'admin')")

        conn.commit()
        conn.close()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()

        tk.Label(self.root, text="Логин:").pack()
        self.login_entry = tk.Entry(self.root)
        self.login_entry.pack()

        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Войти", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Выйти", command=self.root.quit).pack()

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect("medical.db")
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE login=? AND password=?", (login, password))
        user = cur.fetchone()
        conn.close()

        if user:
            self.role = user[0]
            self.show_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Вы вошли как: {self.role}").pack(pady=10)

        if self.role == "admin":
            tk.Button(self.root, text="Добавить болезнь", command=self.add_disease).pack(pady=5)
            tk.Button(self.root, text="Список болезней", command=self.show_diseases).pack(pady=5)

        tk.Button(self.root, text="Выйти", command=self.show_login).pack(pady=10)

    def add_disease(self):
        self.clear_screen()

        tk.Label(self.root, text="Название болезни:").pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        tk.Label(self.root, text="Описание:").pack()
        desc_entry = tk.Entry(self.root)
        desc_entry.pack()

        def save():
            conn = sqlite3.connect("medical.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO diseases (name, description) VALUES (?, ?)",
                        (name_entry.get(), desc_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Болезнь добавлена")
            self.show_main_menu()

        tk.Button(self.root, text="Сохранить", command=save).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.show_main_menu).pack()

    def show_diseases(self):
        self.clear_screen()

        conn = sqlite3.connect("medical.db")
        cur = conn.cursor()
        cur.execute("SELECT name, description FROM diseases")
        diseases = cur.fetchall()
        conn.close()

text = tk.Text(self.root)
text.pack(fill="both", expand=True)

for name, desc in diseases:
    text.insert("end", f"{name}: {desc}\n\n")

tk.Button(self.root, text="Назад", command=self.show_main_menu).pack()

# Запуск приложения
app = SimpleMedicalApp()
app.root.mainloop()