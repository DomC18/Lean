import globalvariables
import tkinter as tk
import constants
import projutil
import json

def verify_existing(root:tk.Tk, first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, first_label:tk.Label, user_label:tk.Label, password_label:tk.Label, task_func) -> None:
    data:dict = {}
    name = first_entry.get()

    name_invalid = first_entry.get() == ""
    username_invalid = user_entry.get() == ""
    password_invalid = password_entry.get() == ""

    if name_invalid:
        first_label.configure(fg_color="red")
    else: 
        first_label.configure(fg_color="black")

    if username_invalid:
        user_label.configure(fg_color="red")
    else: 
        user_label.configure(fg_color="black")

    if password_invalid:
        password_label.configure(fg_color="red")
    else: 
        password_label.configure(fg_color="black")
    
    file_dir = constants.USERDATADIR + rf"{name}.json"
    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        register_new(root, first_entry, user_entry, password_entry, task_func)
        return
        
    username = data[name]["username"]
    password = data[name]["password"]

    globalvariables.name = name
    globalvariables.username = username
    globalvariables.password = password

    if username == user_entry.get() and password == password_entry.get():
        root.destroy()
        projutil.load_creds()
        task_func()

def register_new(root:tk.Tk, first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, task_func) -> None:
    name = first_entry.get()

    if name == "":
        return

    username = user_entry.get()
    password = password_entry.get()

    file_dir = constants.USERDATADIR + rf"{name}.json"

    user_data = {
        name: {
            "username": username,
            "password": password
        },
        "projects": [
            
        ]
    }

    globalvariables.name = name
    globalvariables.username = username
    globalvariables.password = password

    with open(file_dir, "w") as file:
        json.dump(user_data, file, indent=4)

    root.destroy()
    task_func()