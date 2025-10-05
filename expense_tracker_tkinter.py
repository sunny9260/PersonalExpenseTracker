import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Optional OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# === CONFIG ===
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATA_PATH = DATA_DIR / "expenses.csv"

# === FUNCTIONS ===
def load_data():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["Category", "Amount", "Date"])

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

def add_expense():
    category = category_var.get()
    amount = amount_var.get()
    date = date_var.get()

    if not category or not amount:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    new_expense = pd.DataFrame([[category, amount, date]], columns=["Category", "Amount", "Date"])
    df = load_data()
    df = pd.concat([df, new_expense], ignore_index=True)
    save_data(df)
    update_table()
    update_summary()
    messagebox.showinfo("Success", "Expense added successfully!")

def update_table():
    for i in table.get_children():
        table.delete(i)
    df = load_data()
    for index, row in df.iterrows():
        table.insert("", "end", values=list(row))

def update_summary():
    df = load_data()
    if df.empty:
        summary_label.config(text="No data available")
        return
    total = df["Amount"].sum()
    category_sum = df.groupby("Category")["Amount"].sum()
    summary_text = f"Total Expenses: ₹{total:.2f}\n\n"
    for cat, amt in category_sum.items():
        summary_text += f"{cat}: ₹{amt:.2f}\n"
    summary_label.config(text=summary_text)

def clear_all():
    if not messagebox.askyesno("Confirm", "Are you sure you want to delete all data?"):
        return
    if DATA_PATH.exists():
        DATA_PATH.unlink()
    update_table()
    update_summary()
    messagebox.showinfo("Cleared", "All expenses deleted successfully!")

def export_csv():
    df = load_data()
    if df.empty:
        messagebox.showinfo("No Data", "No data to export!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Exported", f"Data exported to {file_path}")

def get_ai_advice():
    if not OPENAI_AVAILABLE:
        messagebox.showerror("Error", "OpenAI not installed! Run `pip install openai`.")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        messagebox.showwarning("No Key", "Please set your OPENAI_API_KEY in .env file.")
        return

    df = load_data()
    if df.empty:
        messagebox.showinfo("No Data", "Add some expenses first!")
        return

    summary_text = f"Total expenses: ₹{df['Amount'].sum():.2f}\n"
    summary_text += "Category-wise: " + ", ".join([f"{c}: ₹{a:.2f}" for c, a in df.groupby('Category')['Amount'].sum().items()])

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial assistant giving concise spending advice."},
                {"role": "user", "content": f"Here are my expenses:\n{summary_text}\nGive me 3 short financial tips."}
            ],
            max_tokens=120
        )
        advice = response.choices[0].message.content.strip()
        messagebox.showinfo("AI Financial Advice", advice)
    except Exception as e:
        messagebox.showerror("OpenAI Error", str(e))

# === MAIN WINDOW ===
root = tk.Tk()
root.title("💰 Personal Expense Tracker (Tkinter + AI)")
root.geometry("700x600")
root.resizable(False, False)

# --- Input Section ---
frame_input = ttk.LabelFrame(root, text="Add Expense")
frame_input.pack(fill="x", padx=10, pady=10)

ttk.Label(frame_input, text="Category:").grid(row=0, column=0, padx=5, pady=5)
category_var = tk.StringVar(value="Food")
category_menu = ttk.Combobox(frame_input, textvariable=category_var,
                             values=["Food", "Rent", "Travel", "Shopping", "Entertainment", "Other"])
category_menu.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Amount (₹):").grid(row=0, column=2, padx=5, pady=5)
amount_var = tk.StringVar()
ttk.Entry(frame_input, textvariable=amount_var, width=10).grid(row=0, column=3, padx=5, pady=5)

ttk.Label(frame_input, text="Date:").grid(row=0, column=4, padx=5, pady=5)
date_var = tk.StringVar(value=datetime.date.today().isoformat())
ttk.Entry(frame_input, textvariable=date_var, width=12).grid(row=0, column=5, padx=5, pady=5)

ttk.Button(frame_input, text="Add", command=add_expense).grid(row=0, column=6, padx=5, pady=5)

# --- Table Section ---
frame_table = ttk.LabelFrame(root, text="Expense Records")
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Category", "Amount", "Date")
table = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=150)
table.pack(fill="both", expand=True)

# --- Summary Section ---
frame_summary = ttk.LabelFrame(root, text="Summary")
frame_summary.pack(fill="x", padx=10, pady=10)
summary_label = ttk.Label(frame_summary, text="", justify="left")
summary_label.pack(padx=10, pady=5)

# --- Buttons Section ---
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

ttk.Button(frame_buttons, text="Update Summary", command=update_summary).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Export CSV", command=export_csv).grid(row=0, column=1, padx=5)
ttk.Button(frame_buttons, text="Clear All Data", command=clear_all).grid(row=0, column=2, padx=5)
ttk.Button(frame_buttons, text="Get AI Advice ", command=get_ai_advice).grid(row=0, column=3, padx=5)

# Load initial data
update_table()
update_summary()

root.mainloop()
