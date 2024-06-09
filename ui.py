from fileutil import verify_existing
import customtkinter as ctk

root : ctk.CTk

def rgb_to_hex(rgb:tuple) -> str:
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def init() -> None:
    root = ctk.CTk(rgb_to_hex((71,0,0))) #maroon
    root.title = "Lean"
    root.resizable(width=False, height=False)
    width = 1040
    height = 585
    horiz_offset = (root.winfo_screenwidth() - width) / 2
    vert_offset = (root.winfo_screenheight() - height) / 2
    root.geometry(f"{width}x{height}+{int(horiz_offset)}+{int(vert_offset)}")

    logo_label = ctk.CTkLabel(root, text="Lean Login", font=("Arial", 80), bg_color=rgb_to_hex((71,0,0)), width=1200, height=150)
    logo_label.place(relx=0.5, rely=0, anchor="n")

    firstname_label = ctk.CTkLabel(root, text="*First Name:", font=("Arial", 50), bg_color=rgb_to_hex((71,0,0)), width=100, height=100)
    firstname_label.place(relx=0.125, rely=0.325, anchor="w")

    firstname_entry = ctk.CTkEntry(root, font=("Arial", 50), width=500, height=100)
    firstname_entry.place(relx=0.875, rely=0.325, anchor="e")

    username_label = ctk.CTkLabel(root, text="*Username:", font=("Arial", 50), bg_color=rgb_to_hex((71,0,0)), width=100, height=100)
    username_label.place(relx=0.125, rely=0.5, anchor="w")

    username_entry = ctk.CTkEntry(root, font=("Arial", 50), width=500, height=100)
    username_entry.place(relx=0.875, rely=0.5, anchor="e")

    password_label = ctk.CTkLabel(root, text="*Password:", font=("Arial", 50), bg_color=rgb_to_hex((71,0,0)), width=100, height=100)
    password_label.place(relx=0.125, rely=0.675, anchor="w")

    password_entry = ctk.CTkEntry(root, font=("Arial", 50), width=500, height=100)
    password_entry.place(relx=0.875, rely=0.675, anchor="e")

    login_button = ctk.CTkButton(root, text="Login/Register", font=("Arial", 50), bg_color="green", fg_color="black", width=15, height=75, command=lambda r=root, f=firstname_entry, u=username_entry, p=password_entry, fl=firstname_label, ul=username_label, pl=password_label, func=init_create : verify_existing(r,f,u,p,fl,ul,pl,func))
    login_button.place(relx=0.5, rely=0.95, anchor="s")

    def exit(event) -> None:
        root.destroy()

    root.bind("<Escape>", exit)
    root.mainloop()

def init_create() -> None:
    ...