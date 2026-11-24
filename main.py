import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def init_db():
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            remind_at TEXT NOT NULL,
            status TEXT DEFAULT 'Ожидает'
        )
    """)

    conn.commit()
    conn.close()


init_db()

print("База данных успешно создана!")
root = tk.Tk()
root.title("Мои напоминания")
root.geometry("900x550")
root.configure(bg="#F5F5F5")

heading = tk.Label(
    root,
    text="Мои напоминания",
    font=("Segoe UI", 24, "bold"),
    bg="#F5F5F5"
)

heading.pack(pady=20)
form = ttk.Frame(root, padding=15)
form.pack(fill="x", padx=20)

ttk.Label(form, text="Заголовок:").pack(anchor="w")
title_entry = ttk.Entry(form)
title_entry.pack(fill="x", pady=5)

ttk.Label(form, text="Описание:").pack(anchor="w")
description_entry = ttk.Entry(form)
description_entry.pack(fill="x", pady=5)

ttk.Label(form, text="Дата (ДД.ММ.ГГГГ):").pack(anchor="w")
date_entry = ttk.Entry(form)
date_entry.pack(fill="x", pady=5)

ttk.Label(form, text="Время (ЧЧ:ММ):").pack(anchor="w")
time_entry = ttk.Entry(form)
time_entry.pack(fill="x", pady=5)
def add_reminder():
    title = title_entry.get().strip()
    description = description_entry.get()
    date = date_entry.get()
    time = time_entry.get()

    if not title:
        messagebox.showerror("Ошибка", "Введите заголовок")
        return

    try:
        remind_at = datetime.strptime(
            date + " " + time, "%d.%m.%Y %H:%M"
        )
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте дату и время")
        return

    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders
        (title, description, remind_at, status)
        VALUES (?, ?, ?, ?)
    """, (
        title,
        description,
        remind_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Ожидает"
    ))

    conn.commit()
    conn.close()

    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    load_reminders()    
    messagebox.showinfo("Успешно", "Напоминание добавлено!")


add_button = ttk.Button(
    form,
    text="Добавить напоминание",
    command=add_reminder
)

add_button.pack(pady=15)
root.geometry("1000x600")

columns = ("id", "title", "description", "remind_at", "status")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=5
)

tree.heading("id", text="ID")
tree.heading("title", text="Заголовок")
tree.heading("description", text="Описание")
tree.heading("remind_at", text="Дата и время")
tree.heading("status", text="Статус")

tree.column("id", width=40)
tree.column("title", width=200)
tree.column("description", width=300)
tree.column("remind_at", width=160)
tree.column("status", width=120)

tree.pack(fill="both", expand=True, padx=20, pady=10)


def load_reminders():
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    status = status_filter.get()

    if status == "Все":
        cursor.execute("""
            SELECT id, title, description, remind_at, status
            FROM reminders
            ORDER BY remind_at
        """)
    else:
        cursor.execute("""
            SELECT id, title, description, remind_at, status
            FROM reminders
            WHERE status = ?
            ORDER BY remind_at
        """, (status,))

    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()


def get_selected_id():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Внимание",
            "Выберите напоминание!"
        )
        return None

    return tree.item(selected[0])["values"][0]


def delete_reminder():
    reminder_id = get_selected_id()

    if reminder_id is None:
        return

    if not messagebox.askyesno(
        "Удаление",
        "Удалить напоминание?"
    ):
        return

    conn = sqlite3.connect("reminders.db")
    conn.execute(
        "DELETE FROM reminders WHERE id = ?",
        (reminder_id,)
    )
    conn.commit()
    conn.close()

    load_reminders()


def change_status(status):
    reminder_id = get_selected_id()

    if reminder_id is None:
        return

    conn = sqlite3.connect("reminders.db")
    conn.execute(
        "UPDATE reminders SET status = ? WHERE id = ?",
        (status, reminder_id)
    )
    conn.commit()
    conn.close()

    load_reminders()


buttons_frame = tk.Frame(root)
buttons_frame.pack(before=tree, pady=5)

tk.Button(
    buttons_frame,
    text="Готово",
    bg="#4CAF50",
    fg="white",
    width=15,
    command=lambda: change_status("Готово")
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="Отменить",
    bg="#757575",
    fg="white",
    width=15,
    command=lambda: change_status("Отменено")
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="Удалить",
    bg="#D32F2F",
    fg="white",
    width=15,
    command=delete_reminder
).pack(side="left", padx=5)


def get_selected_id():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Внимание",
            "Выберите напоминание!"
        )
        return None

    return tree.item(selected[0])["values"][0]


def delete_reminder():
    reminder_id = get_selected_id()

    if reminder_id is None:
        return

    if not messagebox.askyesno(
        "Удаление",
        "Удалить напоминание?"
    ):
        return

    conn = sqlite3.connect("reminders.db")
    conn.execute(
        "DELETE FROM reminders WHERE id = ?",
        (reminder_id,)
    )
    conn.commit()
    conn.close()

    load_reminders()


def change_status(status):
    reminder_id = get_selected_id()

    if reminder_id is None:
        return

    conn = sqlite3.connect("reminders.db")
    conn.execute(
        "UPDATE reminders SET status = ? WHERE id = ?",
        (status, reminder_id)
    )
    conn.commit()
    conn.close()

    load_reminders()


buttons_frame = tk.Frame(root)
buttons_frame.pack(side="bottom", pady=10)

tk.Button(
    buttons_frame,
    text="Готово",
    bg="#4CAF50",
    fg="white",
    width=15,
    command=lambda: change_status("Готово")
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="Отменить",
    bg="#757575",
    fg="white",
    width=15,
    command=lambda: change_status("Отменено")
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="Удалить",
    bg="#D32F2F",
    fg="white",
    width=15,
    command=delete_reminder
).pack(side="left", padx=5)


def get_selected_id():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Внимание",
            "Выберите напоминание!"
        )
        return None

    return tree.item(selected[0])["values"][0]


def delete_reminder():
    reminder_id = get_selected_id()

    if reminder_id is None:
        return

    if not messagebox.askyesno(
        "Удаление",
        "Удалить напоминание?"
    ):
        return

    conn = sqlite3.connect("reminders.db")
    conn.execute(
        "DELETE FROM reminders WHERE id = ?",
        (reminder_id,)
    )
    conn.commit()
    conn.close()

    load_reminders()


def change_status(status):
    reminder_id = get_selected_id()

    if reminder_id is None:
        return

    conn = sqlite3.connect("reminders.db")
    conn.execute(
        "UPDATE reminders SET status = ? WHERE id = ?",
        (status, reminder_id)
    )
    conn.commit()
    conn.close()

    load_reminders()


buttons_frame = tk.Frame(root)
buttons_frame.pack(side="bottom", pady=10)

tk.Button(
    buttons_frame,
    text="Готово",
    bg="#4CAF50",
    fg="white",
    width=15,
    command=lambda: change_status("Готово")
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="Отменить",
    bg="#757575",
    fg="white",
    width=15,
    command=lambda: change_status("Отменено")
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="Удалить",
    bg="#D32F2F",
    fg="white",
    width=15,
    command=delete_reminder
).pack(side="left", padx=5)


filter_frame = tk.Frame(root)
filter_frame.pack(before=tree, pady=5)

tk.Label(
    filter_frame,
    text="Фильтр по статусу:"
).pack(side="left", padx=5)

status_filter = ttk.Combobox(
    filter_frame,
    values=[
        "Все",
        "Ожидает",
        "Готово",
        "Просрочено",
        "Отменено"
    ],
    state="readonly",
    width=20
)

status_filter.set("Все")
status_filter.pack(side="left")

status_filter.bind(
    "<<ComboboxSelected>>",
    lambda event: load_reminders()
)

def show_notification(title, description):
    popup = tk.Toplevel(root)
    popup.title("Напоминание")
    popup.geometry("400x220")
    popup.attributes("-topmost", True)

    tk.Label(
        popup,
        text="Время напоминания!",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    tk.Label(
        popup,
        text=title,
        font=("Arial", 14)
    ).pack(pady=5)

    tk.Label(
        popup,
        text=description,
        wraplength=350
    ).pack(pady=5)

    tk.Button(
        popup,
        text="Закрыть",
        command=popup.destroy
    ).pack(pady=15)

    popup.lift()
    popup.bell()


def check_reminders():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description
        FROM reminders
        WHERE status = 'Ожидает'
        AND remind_at <= ?
    """, (now,))

    overdue = cursor.fetchall()

    for reminder_id, title, description in overdue:
        cursor.execute("""
            UPDATE reminders
            SET status = 'Просрочено'
            WHERE id = ?
        """, (reminder_id,))

    conn.commit()
    conn.close()

    if overdue:
        load_reminders()

        for reminder_id, title, description in overdue:
            show_notification(title, description)

    root.after(5000, check_reminders)


load_reminders()
check_reminders()
root.mainloop()