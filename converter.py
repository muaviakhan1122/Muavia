import tkinter as tk
from tkinter import messagebox

# Function to convert text to binary
def text_to_binary():
    text = text_entry.get()
    if not text:
        messagebox.showerror("Error", "Please enter some text!")
        return
    binary_result = ' '.join(format(ord(char), '08b') for char in text)
    result_label.config(text=f"Binary: {binary_result}")
# Function to convert binary to text
def binary_to_text():
    binary = text_entry.get()
    try:
        words = binary.split()
        text_result = ''.join(chr(int(b, 2)) for b in words)
        result_label.config(text=f"Text: {text_result}")
    except ValueError:
        messagebox.showerror("Error", "Invalid binary input!")
# GUI setup
root = tk.Tk()
root.title("Text-Binary Converter")
root.geometry("400x300")
# Input field
tk.Label(root, text="Enter Text or Binary:").pack(pady=5)
text_entry = tk.Entry(root, width=40)
text_entry.pack(pady=5)
# Button
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Convert to Binary", command=text_to_binary).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Convert to Text", command=binary_to_text).pack(side=tk.LEFT, padx=5)
# Result Label
result_label = tk.Label(root, text="", wraplength=350)
result_label.pack(pady=10)
# Run the GUI
root.mainloop()
