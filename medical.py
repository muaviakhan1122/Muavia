import csv
import tkinter as tk
from tkinter import ttk, messagebox

# Convert to lowercase
def to_lower_case(s):
    return s.lower()

# Check symptom match (50% threshold)
def match_symptoms(disease_symptoms, user_symptoms):
    match_count = sum(1 for symptom in user_symptoms if symptom in disease_symptoms)
    return match_count >= len(user_symptoms) // 2  

# Load diseases from CSV file
def load_diseases(file_path):
    diseases = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Ensure row is not empty
                    disease_name = to_lower_case(row[0])
                    symptoms = [to_lower_case(symptom) for symptom in row[1:] if symptom]
                    diseases[disease_name] = symptoms
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
    return diseases

# Find matching disease
def find_disease():
    user_input = entry.get().strip()
    
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter at least one symptom.")
        return
    
    user_symptoms = [to_lower_case(symptom.strip()) for symptom in user_input.split(',')]
    possible_diseases = [disease for disease, symptoms in diseases.items() if match_symptoms(symptoms, user_symptoms)]
    
    if possible_diseases:
        result = "Possible diseases based on your symptoms:\n" + "\n".join(possible_diseases)
    else:
        result = "No exact match found. Consider consulting a doctor."
    
    messagebox.showinfo("Diagnosis Result", result)

# Load disease data
file_path = r"C:\Users\USER\Documents\Book1.csv"  # Update the path accordingly
diseases = load_diseases(file_path)

# GUI Setup
root = tk.Tk()
root.title("Disease Symptom Matcher")
root.geometry("500x350")
root.configure(bg="#f9f9f9")

# Custom font
custom_font = ("Helvetica", 12)

# Header label
header_label = tk.Label(
    root,
    text="Disease Symptom Matcher",
    font=("Helvetica", 16, "bold"),
    bg="#f9f9f9",
    fg="#333333"
)
header_label.pack(pady=10)

# Instruction label
instruction_label = tk.Label(
    root,
    text="Enter your symptoms (comma-separated):",
    font=custom_font,
    bg="#f9f9f9",
    fg="#555555"
)
instruction_label.pack(pady=5)

# Entry widget
entry = ttk.Entry(root, width=50, font=custom_font)
entry.pack(pady=10, ipady=5)

# Button styling
style = ttk.Style()
style.configure("Accent.TButton", font=custom_font, background="#4CAF50", foreground="white")
style.map("Accent.TButton", background=[("active", "#45a049")])

# Find disease button
find_button = ttk.Button(root, text="Find Disease", command=find_disease, style="Accent.TButton")
find_button.pack(pady=10)

# Run the application
root.mainloop()
