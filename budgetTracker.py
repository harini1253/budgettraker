import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class BudgetTrackerApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Budget Tracker")

        self.categories = {}
        self.transactions = []

        self.load_transactions('transactions.json')

        self.create_widgets()

    def create_widgets(self):
        self.category_label = tk.Label(self.master, text="Category:")
        self.category_label.grid(row=0, column=0, padx=5, pady=5)

        self.category_entry = tk.Entry(self.master)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)

        self.amount_label = tk.Label(self.master, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=5, pady=5)

        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.income_button = tk.Button(self.master, text="Add Income", command=self.add_income)
        self.income_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.expense_button = tk.Button(self.master, text="Add Expense", command=self.add_expense)
        self.expense_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.remaining_budget_button = tk.Button(self.master, text="Calculate Remaining Budget", command=self.calculate_budget)
        self.remaining_budget_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.expense_analysis_button = tk.Button(self.master, text="Expense Analysis", command=self.expense_analysis)
        self.expense_analysis_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def add_income(self):
        category = self.category_entry.get()
        amount = float(self.amount_entry.get())
        self.add_transaction(category, amount, 'income')
        messagebox.showinfo("Success", "Income added successfully.")

    def add_expense(self):
        category = self.category_entry.get()
        amount = float(self.amount_entry.get())
        self.add_transaction(category, amount, 'expense')
        messagebox.showinfo("Success", "Expense added successfully.")

    def add_transaction(self, category, amount, transaction_type):
        if category in self.categories:
            if transaction_type == 'income':
                self.transactions.append({'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          'category': category,
                                          'amount': amount,
                                          'type': transaction_type})
            elif transaction_type == 'expense':
                if self.categories[category] >= amount:
                    self.transactions.append({'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              'category': category,
                                              'amount': amount,
                                              'type': transaction_type})
                    self.categories[category] -= amount
                else:
                    messagebox.showerror("Error", "Insufficient funds in this category.")
        else:
            messagebox.showerror("Error", "Category not found.")

    def calculate_budget(self):
        total_income = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'income')
        total_expense = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'expense')
        remaining_budget = total_income - total_expense
        messagebox.showinfo("Remaining Budget", f"Remaining Budget: ${remaining_budget}")

    def expense_analysis(self):
        expense_categories = {}
        for transaction in self.transactions:
            if transaction['type'] == 'expense':
                category = transaction['category']
                amount = transaction['amount']
                if category in expense_categories:
                    expense_categories[category] += amount
                else:
                    expense_categories[category] = amount
        messagebox.showinfo("Expense Analysis", f"Expense Analysis: {expense_categories}")

    def save_transactions(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.transactions, f)

    def load_transactions(self, filename):
        try:
            with open(filename, 'r') as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            pass


def main():
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()


if __name__ == "_main_":
    main()