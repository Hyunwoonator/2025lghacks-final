import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
from PIL import Image, ImageTk

# Define a consistent color scheme
colors = {
    "black": "#121212",
    "blue": "#007BFF",
    "purple": "#8A2BE2",
    "charcoal": "#1E1E2E",
    "lavender": "#C084FC"
}

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1000x500")
app.title("Clarus: AI-powered file organization.")
app.configure(fg_color=colors["black"])

# Functions
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_text.delete(0, "end")
        directory_text.insert(0, directory)
        print(directory)

def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if directory_text.get() == 'Enter a directory...':
       directory_text.delete(0, "end") # delete all the text in the entry
       directory_text.insert(0, '') #Insert blank for user input
       directory_text.configure(text_color="white")

def on_focusout(event):
    if directory_text.get() == '':
        directory_text.insert(0, 'Enter a directory...')
        directory_text.configure(text_color="gray")


def on_enter_submit(event):
    print(directory_text.get())
    try:
        subprocess.Popen(["python", "main.py"])
    except:
        subprocess.Popen(["python3","main.py"])
    app.destroy()

def on_click_submit():
    print(directory_text.get())
    try:
        subprocess.Popen(["python", "main.py"])
    except:
        subprocess.Popen(["python3", "main.py"])
    app.destroy()

# Create a frame for better organization
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(expand=True, fill="both")

# Logo and title
title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
title_frame.pack(pady=(80, 20))

greeting_text = ctk.CTkLabel(
    title_frame, 
    text="Clarus", 
    font=("Tahoma", 50, "bold"),
    text_color=colors["lavender"]
)
greeting_text.pack()

subtitle = ctk.CTkLabel(
    title_frame,
    text="AI-powered file organization",
    font=("Tahoma", 16),
    text_color="light gray"
)
subtitle.pack(pady=(0, 20))

# Input section
input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
input_frame.pack(pady=20)

directory_text = ctk.CTkEntry(
    input_frame, 
    width=400, 
    height=40,
    corner_radius=8,
    border_width=2,
    border_color=colors["charcoal"],
    fg_color=colors["charcoal"],
    text_color="gray",
    font=("Tahoma", 14)
)
directory_text.insert(0, 'Enter a directory...')
directory_text.bind('<FocusIn>', on_entry_click)
directory_text.bind('<FocusOut>', on_focusout)
directory_text.bind('<Return>', on_enter_submit)
directory_text.pack(pady=20)

# Buttons section
button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
button_frame.pack(pady=10)

directory_btn = ctk.CTkButton(
    button_frame, 
    text="Choose Directory", 
    command=select_directory, 
    font=("Tahoma", 16),
    fg_color=colors["blue"],
    hover_color="#0069d9",
    corner_radius=8,
    width=200,
    height=40
)
directory_btn.pack(side="left", padx=10)

submit_btn = ctk.CTkButton(
    button_frame, 
    text="Confirm", 
    command=on_click_submit, 
    font=("Tahoma", 16),
    fg_color=colors["charcoal"],
    hover_color=colors["lavender"],
    corner_radius=8,
    width=200,
    height=40
)
submit_btn.pack(side="left", padx=10)

# Footer
footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
footer_frame.pack(pady=(60, 0))

footer_text = ctk.CTkLabel(
    footer_frame,
    text="© 2025 Clarus",
    font=("Tahoma", 12),
    text_color="gray"
)
footer_text.pack()

app.mainloop()