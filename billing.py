import tkinter as tk
from tkinter import messagebox
import datetime

# Function to calculate totals
def calculate_total():
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        paid = float(paid_entry.get())
        cost = float(cost_entry.get())
        
        subtotal = price * quantity
        total_label.config(text=f"Total: {subtotal:.2f}")
        
        remaining = paid - subtotal
        remaining_label.config(text=f"Remaining: {remaining:.2f}")
        
        profit = (price - cost) * quantity
        profit_label.config(text=f"Profit: {profit:.2f}")
        
        save_transaction(price, quantity, subtotal, paid, remaining, profit)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values!")

# Function to save transactions to history file
def save_transaction(price, quantity, total, paid, remaining, profit):
    with open("history.txt", "a") as file:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{date_time}, Price: {price}, Quantity: {quantity}, Total: {total}, Paid: {paid}, Remaining: {remaining}, Profit: {profit}\n")
    messagebox.showinfo("Success", "Transaction saved successfully!")

# GUI Setup
root = tk.Tk()
root.title("Supermarket Billing System")
root.geometry("400x400")

tk.Label(root, text="Price per Item:").pack()
price_entry = tk.Entry(root)
price_entry.pack()

tk.Label(root, text="Quantity:").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

tk.Label(root, text="Amount Paid:").pack()
paid_entry = tk.Entry(root)
paid_entry.pack()

tk.Label(root, text="Cost per Item:").pack()
cost_entry = tk.Entry(root)
cost_entry.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate_total)
calculate_button.pack()

total_label = tk.Label(root, text="Total: 0.00")
total_label.pack()

remaining_label = tk.Label(root, text="Remaining: 0.00")
remaining_label.pack()

profit_label = tk.Label(root, text="Profit: 0.00")
profit_label.pack()

root.mainloop()
