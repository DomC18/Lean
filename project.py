from tkinter import filedialog
import customtkinter as ctk
import constants

class Project(ctk.CTkFrame):
    def __init__(self, window:ctk.CTk, width=0, height=0, bg_color="#470000", name="", **kwargs) -> None:
        super().__init__(master=window, width=width, height=height, bg_color=bg_color, **kwargs)
        self.place(anchor="center", relx=0.5, rely=0.5)

        self.window = window
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.name = name

        self.util_frame = ctk.CTkFrame(master=self, width=width, height=height*0.1, fg_color=bg_color, border_width=2)
        self.util_frame.place(anchor="n", relx=0.5, rely=0)
        self.file_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="File", font=("Arial", 50, "bold"), border_width=1)
        self.file_button.configure(command=self.file_expand)
        self.file_button.place(anchor="w", relx=0, rely=0.5)
        self.new_button = ctk.CTkButton(master=self, width=width*0.1, height=height*0.095, fg_color=bg_color, text="New", font=("Arial", 50, "bold"), border_width=1)
        self.new_button.configure(command=self.new_project)
        self.open_button = ctk.CTkButton(master=self, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Open", font=("Arial", 50, "bold"), border_width=1)
        self.open_button.configure(command=self.open_project)
        self.save_button = ctk.CTkButton(master=self, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Save", font=("Arial", 50, "bold"), border_width=1)
        self.save_button.configure(command=self.save)
        self.saveas_button = ctk.CTkButton(master=self, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Save As", font=("Arial", 50, "bold"), border_width=1)
        self.saveas_button.configure(command=self.save_as)
        self.edit_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Edit", font=("Arial", 50, "bold"), border_width=1)
        self.edit_button.configure(command=self.edit_expand)
        self.edit_button.place(anchor="w", relx=0.1, rely=0.5)
        self.import_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Import", font=("Arial", 50, "bold"), border_width=1)
        self.import_button.configure(command=self.import_img)
        self.import_button.place(anchor="w", relx=0.2, rely=0.5)
        self.undo_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="←Undo", font=("Arial", 50, "bold"), border_width=1)
        self.undo_button.configure(command=self.undo)
        self.undo_button.place(anchor="w", relx=0.3, rely=0.5)
        self.redo_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Redo→", font=("Arial", 50, "bold"), border_width=1)
        self.redo_button.configure(command=self.redo)
        self.redo_button.place(anchor="w", relx=0.4111, rely=0.5)
        self.raise_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="↑ Raise", font=("Arial", 50, "bold"), border_width=1)
        self.raise_button.configure(command=self.raise_element)
        self.raise_button.place(anchor="w", relx=0.52, rely=0.5)
        self.back_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Main Menu", font=("Arial", 50, "bold"), border_width=1)
        self.back_button.configure(command=self.destruct)
        self.back_button.place(anchor="e", relx=1, rely=0.5)

        self.tool_frame = ctk.CTkFrame(master=self, width=width, height=height*0.18, fg_color=bg_color, border_width=2)
        self.tool_frame.place(anchor="n", relx=0.5, rely=0.1)

        self.drawing_frame = ctk.CTkFrame(master=self, width=width, height=height*0.72, fg_color=bg_color, border_width=2)
        self.drawing_frame.place(anchor="n", relx=0.5, rely=0.28)
    
    def file_expand(self) -> None:
        self.file_button.configure(command=self.file_collapse)
        self.new_button.place(anchor="w", relx=0, rely=0.145)
        self.new_button.tkraise()
        self.open_button.place(anchor="w", relx=0, rely=0.24)
        self.open_button.tkraise()
        self.save_button.place(anchor="w", relx=0, rely=0.335)
        self.save_button.tkraise()
        self.saveas_button.place(anchor="w", relx=0, rely=0.43)
        self.saveas_button.tkraise()

    def file_collapse(self) -> None:
        self.file_button.configure(command=self.file_expand)
        self.new_button.place_forget()
        self.open_button.place_forget()
        self.save_button.place_forget()
        self.saveas_button.place_forget()

    def new_project(self) -> None:
        ...

    def open_project(self) -> None:
        ...

    def save(self) -> None:
        ...

    def save_as(self) -> None:
        ...

    def edit_expand(self) -> None:
        ...

    def edit_collapse(self) -> None:
        ...

    def cut(self) -> None:
        ...
    
    def copy(self) -> None:
        ...
    
    def paste(self) -> None:
        ...

    def import_img(self) -> None:
        file_path = filedialog.askopenfilename(
            initialdir=rf"{constants.PUBLICDIR}",
            title="Select an image",
            filetypes=(("PNGs", "*.png"), ("JPGs", "*.jpg"), ("All files", "*.*"))
        )
        if file_path:
            ...

    def undo(self) -> None:
        ...

    def redo(self) -> None:
        ...

    def raise_element(self, element) -> None:
        ...

    def select(self) -> None:
        ...
    
    def select_elements(self) -> None:
        ...

    def select_all(self) -> None:
        ...

    def pencil(self) -> None:
        ...
    
    def erase(self) -> None:
        ...
    
    def change_draw_size(self) -> None:
        ...
    
    def fill(self) -> None:
        ...
    
    def eyedrop(self) -> None:
        ...

    def insert_text(self) -> None:
        ...

    def select_element(self) -> None:
        ...
    
    def place_element(self) -> None:
        ...
    
    def resize_element(self) -> None:
        ...
    
    def rotate_element(self) -> None:
        ...

    def select_color(self) -> None:
        ...
    
    def pick_color(self) -> None:
        ...

    def destruct(self) -> None:
        self.destroy()

    def build_elements(self, elements) -> None:
        ...

    def as_dict(self) -> dict:
        return {
            self.name: {
                "name": self.name,
                "elements": self.elements,
            }
        }