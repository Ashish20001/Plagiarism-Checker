import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher

def load_file_or_display_contents(entry, text_widget):
    file_path = entry.get()

    if not file_path:
        file_path = filedialog.askopenfilename()

    if file_path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, file_path)
        with open(file_path, 'r') as file:
            text = file.read()
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, text)

def compare_text(text1, text2):
    d = SequenceMatcher(None, text1, text2)
    similarity_ratio = d.ratio()
    similarity_percentage = int(similarity_ratio * 100)

    diff = list(d.get_opcodes())
    return similarity_percentage, diff

def show_similarity():
    text1 = text_textbox1.get(1.0, tk.END)
    text2 = text_textbox2.get(1.0, tk.END)
    similarity_percentage, diff = compare_text(text1, text2)
    
    text_textbox_diff.delete(1.0, tk.END)
    text_textbox_diff.insert(tk.END, f"Similarity: {similarity_percentage}%")
    
    text_textbox1.tag_remove("same", "1.0", tk.END)
    text_textbox2.tag_remove("same", "1.0", tk.END)
    
    for opcode in diff:
        tag = opcode[0]
        start1, end1, start2, end2 = opcode[1], opcode[2], opcode[3], opcode[4]

        if tag == "equal":
            text_textbox1.tag_add("same", f"1.0+{start1}c", f"1.0+{end1}c")
            text_textbox2.tag_add("same", f"1.0+{start2}c", f"1.0+{end2}c")

def clear_all():
    text_textbox1.delete(1.0, tk.END)
    text_textbox2.delete(1.0, tk.END)
    text_textbox_diff.delete(1.0, tk.END)
    file_entry1.delete(0, tk.END)
    file_entry2.delete(0, tk.END)

root = tk.Tk()
root.title("Plagarism Checker")
root.configure(bg="#F0F0F0")

frame = tk.Frame(root, bg="#E0E0E0")
frame.pack(padx=10, pady=10)

text_label1 = tk.Label(frame, text="Text 1:", bg="#E0E0E0")
text_label1.grid(row=0, column=0, padx=5, pady=5)

text_textbox1 = tk.Text(frame, wrap=tk.WORD, width=40, height=10)
text_textbox1.grid(row=0, column=1, padx=5, pady=5)

text_label2 = tk.Label(frame, text="Text 2:", bg="#E0E0E0")
text_label2.grid(row=0, column=2, padx=5, pady=5)

text_textbox2 = tk.Text(frame, wrap=tk.WORD, width=40, height=10)
text_textbox2.grid(row=0, column=3, padx=5, pady=5)

file_entry1 = tk.Entry(frame, width=50)
file_entry1.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

load_button1 = tk.Button(frame, text="Load File 1", command=lambda: load_file_or_display_contents(file_entry1, text_textbox1), bg="#4CAF50", fg="white")
load_button1.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

file_entry2 = tk.Entry(frame, width=50)
file_entry2.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

load_button2 = tk.Button(frame, text="Load File 2", command=lambda: load_file_or_display_contents(file_entry2, text_textbox2), bg="#4CAF50", fg="white")
load_button2.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

compare_button = tk.Button(root, text="Compare", command=show_similarity, bg="#008CBA", fg="white")
compare_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear All", command=clear_all, bg="#D9534F", fg="white")
clear_button.pack(pady=5)

text_textbox_diff = tk.Text(root, wrap=tk.WORD, width=80, height=1)
text_textbox_diff.pack(padx=10, pady=10)

text_textbox1.tag_configure("same", foreground="red", background="lightyellow")
text_textbox2.tag_configure("same", foreground="red", background="lightyellow")

root.mainloop()
