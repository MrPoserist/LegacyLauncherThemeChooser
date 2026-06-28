import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import sv_ttk
import os

root = tk.Tk()
root.title("Legacy Launcher Theme Chooser")
root.geometry("800x700")

home_dir = os.path.expanduser("~")
path = None
themes_path = None
chosen_theme = None

def choose_path():
    dir = filedialog.askdirectory()
    if dir:
        try:
            with open(f"{dir}/legacy.properties") as file:
                path_label.config(text=f"Legacy Launcher path: {dir}/legacy.properties")
                global path
                path = f"{dir}/legacy.properties"
        except FileNotFoundError:
            path_label.config(text=f"File {dir}/legacy.properties not found")

path_label = ttk.Label(text="Legacy Launcher path: ?")
choose_path_button = ttk.Button(root, text="Choose", command=choose_path)

try:
    with open(f"{home_dir}/.tlauncher/legacy.properties") as file:
        path_label.config(text=f"Legacy Launcher path: {home_dir}/.tlauncher/legacy.properties")
        path = f"{home_dir}/.tlauncher/legacy.properties"
except FileNotFoundError:
    pass

path_label.place(anchor=N, x=400, y=20)
choose_path_button.place(anchor=N, x=400, y=50)

def choose_themes():
    dir = filedialog.askdirectory()
    if dir:
        for item in themes_list.get_children():
            themes_list.delete(item)
        for filename in os.listdir(dir):
            filepath = os.path.join(dir, filename)
            if os.path.isfile(filepath):
                themes_list.insert("", "end", values=(filename, filepath))
        themes_label.config(text=f"Themes path: {dir}")

themes_label = ttk.Label(root, text="Themes path: ?")
choose_themes_button = ttk.Button(root, text="Choose", command=choose_themes)
themes_list = ttk.Treeview(root, columns=("name", "path"), show="headings", selectmode="extended")

try:
    for filename in os.listdir(f"{home_dir}/.tlauncher/themes"):
        filepath = os.path.join(f"{home_dir}/.tlauncher/themes", filename)
        if os.path.isfile(filepath):
            themes_list.insert("", "end", values=(filename, filepath))
    themes_label.config(text=f"Themes path: {home_dir}/.tlauncher/themes")
except FileNotFoundError:
    pass

def theme_select(event):
    selected_items = themes_list.selection()
    for item in selected_items:
        values = themes_list.item(item, 'values')
        global chosen_theme
        chosen_theme = values[1]

themes_label.place(anchor=CENTER, x=400, y=120)
choose_themes_button.place(anchor=CENTER, x=400, y=160)
themes_list.place(anchor=CENTER, width=700, height=380, x=400, y=380)
themes_list.bind("<<TreeviewSelect>>", theme_select)

def apply_theme():
    target_prefix = 'gui.laf.v1.flatlaf.dark'
    new_line = f'gui.laf.v1.flatlaf.dark={chosen_theme}'

    with open(path, 'r') as f:
        lines = f.readlines()
    new_lines = [line for line in lines if not line.strip().startswith(target_prefix)]
    new_lines.append(new_line.strip() + '\n')
    with open(path, 'w') as f:
        f.writelines(new_lines)

    target_prefix = 'gui.laf.v1.flatlaf.light'
    new_line = f'gui.laf.v1.flatlaf.light={chosen_theme}'

    with open(path, 'r') as f:
        lines = f.readlines()
    new_lines = [line for line in lines if not line.strip().startswith(target_prefix)]
    new_lines.append(new_line.strip() + '\n')
    with open(path, 'w') as f:
        f.writelines(new_lines)

apply_theme_button = ttk.Button(root, text="Apply", command=apply_theme)
apply_theme_button.place(anchor=CENTER, x=400, y=660)

sv_ttk.set_theme("dark", root)

root.mainloop()