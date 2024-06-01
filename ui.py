import customtkinter as ctk

root : ctk.CTk

def init() -> None:
    root = ctk.CTk("limegreen")
    root.title = "Lean"
    root.geometry("800x450+0+0")
    root.resizable(width=True, height=True)



    root.mainloop()