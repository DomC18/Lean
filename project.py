from tkinter import messagebox
import globalvariables as gv
import customtkinter as ctk
import constants
import json
import os

class Element:
    def __init__(self, 
                typ:str = "label", 
                relx:float = 0.5, 
                rely:float = 0.5, 

                window:ctk.CTk = ctk.CTk(),
                width:int = 140,
                height:int = 28,
                corner_radius:int = None,
                border_width:int = None,
                border_spacing:int = 2,

                bg_color:str = "transparent",
                fg_color:str = None,
                hover_color:str = None,
                border_color:str = None,
                text_color:str = None,
                text_color_disabled = None,
                placeholder_text_color:str = None,

                background_corner_colors = None,
                round_width_to_even_numbers = None,
                round_height_to_even_numbers = None,

                text:str = "CTkLabel",
                textvariable:ctk.Variable = ctk.Variable(),
                state:str = "normal",
                placeholder_text:str = None,
                font:tuple = None,
                image:ctk.CTkImage = None,
                compound:str = "center",
                hover:bool = True,
                command = None,
                anchor:str = "center", 
                wraplength:int = 0, 
            ) -> None:
        
        self.editable = None
        self.typ = typ
        self.relx = relx
        self.rely = rely
        self.window = window
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.border_width = border_width
        self.border_spacing = border_spacing
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.text_color = text_color
        self.text_color_disabled = text_color_disabled
        self.placeholder_text_color = placeholder_text_color
        self.background_corner_colors = background_corner_colors
        self.round_width_to_even_numbers = round_width_to_even_numbers
        self.round_height_to_even_numbers = round_height_to_even_numbers
        self.text = text
        self.textvariable = textvariable
        self.state = state
        self.placeholder_text = placeholder_text
        self.font = font
        self.image = image
        self.compound = compound
        self.hover = hover
        self.command = command
        self.anchor = anchor
        self.wraplength = wraplength

        self.kwargs = {"width": self.width, 
                       "height": self.height, 
                       "corner_radius": self.corner_radius, 
                       "border_width": self.border_width, 
                       "border_spacing": self.border_spacing, 
                       "bg_color": self.bg_color, 
                       "fg_color": self.fg_color, 
                       "hover_color": self.hover_color, 
                       "border_color": self.border_color, 
                       "text_color": self.text_color, 
                       "text_color_disabled": self.text_color_disabled, 
                       "placeholder_text_color": self.placeholder_text_color, 
                       "background_corner_colors": self.background_corner_colors, 
                       "round_width_to_even_numbers": self.round_width_to_even_numbers, 
                       "round_height_to_even_numbers": self.round_height_to_even_numbers,
                       "text": self.text, 
                       "state": self.state, 
                       "placeholder_text": self.placeholder_text, 
                       "font": self.font, 
                       "image": self.image, 
                       "compound": self.compound, 
                       "hover": self.hover, 
                       "command": self.command, 
                       "anchor": self.anchor, 
                       "wraplength": self.wraplength
        }

        self.apply_config()

    def apply_config(self) -> None:
        try: self.editable.destroy()
        except: pass

        if self.typ == "label":
            self.editable = ctk.CTkLabel(self.window, self.width, self.height, self.corner_radius, self.bg_color, self.fg_color, self.text_color, self.text_color_disabled, self.text, self.font, self.image, self.compound, self.anchor, self.wraplength)
        elif self.typ == "entry":
            self.editable = ctk.CTkEntry(self.window, self.width, self.height, self.corner_radius, self.border_width, self.bg_color, self.fg_color, self.border_color, self.text_color, self.placeholder_text_color, self.textvariable, self.placeholder_text, self.font, self.state)
        elif self.typ == "button":
            self.editable = ctk.CTkButton(self.window, self.width, self.height, self.corner_radius, self.border_width, self.border_spacing, self.bg_color, self.fg_color, self.hover_color, self.border_color, self.text_color, self.text_color_disabled, self.background_corner_colors, self.round_width_to_even_numbers, self.round_height_to_even_numbers, self.text, self.font, self.textvariable, self.image, self.state, self.hover, self.command, self.compound, self.anchor)

    def place(self) -> None:
        self.editable.place(anchor="center", relx=self.relx, rely=self.rely)

    def place_forget(self) -> None:
        self.editable.place_forget()

    def __repr__(self) -> str:
        return f"typ: {self.typ}\nrelx: {self.relx}\nrely: {self.rely}\nkwargs: {self.kwargs}\n"

    def as_dict(self) -> dict:
        return {
            "typ": self.typ,
            "relx": str(self.relx),
            "rely": str(self.rely),
            "kwargs": self.kwargs
        }
        

class Project:
    def __init__(self, name:str="", elements:list[Element]=[]) -> None:
        self.name = name
        self.elements = elements
        
    def name_to(self, new_name:str) -> None:
        self.name = new_name
    
    def element_to(self, old_element:Element, new_element:Element) -> None:
        try: self.elements[self.elements.index(old_element)] = new_element
        except: pass
    
    def add_element(self, element:Element) -> None:
        self.elements.append(element)
    
    def clear_elements(self) -> None:
        self.elements.clear()
    
    def build_elements(self, elements:list) -> None:
        for element in elements:
            self.elements.append(Element(typ=element["typ"], relx=float(element["relx"]), rely=float(element["rely"]), **element["kwargs"]))

    def place_elements(self, parent:ctk.CTkFrame) -> None:
        for element in self.elements:
            element.window = parent
            element.apply_config()
            element.place()

    def __repr__(self) -> str:
        return f"name: {self.name}\nelements: {self.elements}\n"

    def as_dict(self) -> dict:
        return {
            self.name: {
                "name": self.name,
                "elements": [element.as_dict() for element in self.elements],
            }
        }


class ProjectContainer(ctk.CTkFrame):
    def __init__(self, window:ctk.CTk, width=constants.WIDTH, height=constants.HEIGHT, bg_color=constants.MAROON, project=Project(), **kwargs) -> None:
        super().__init__(master=window, width=width, height=height, bg_color=bg_color, **kwargs)
        self.window = window
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.project = project
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
        self.just_saved = True
        self.f_collapse = None

        self.edit_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Edit", font=("Arial", 50, "bold"), border_width=1)
        self.edit_button.configure(command=self.edit_expand)
        self.edit_button.place(anchor="w", relx=0.1, rely=0.5)
        self.cut_button = ctk.CTkButton(master=self, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Cut", font=("Arial", 50, "bold"), border_width=1)
        self.cut_button.configure(command=self.cut)
        self.copy_button = ctk.CTkButton(master=self, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Copy", font=("Arial", 50, "bold"), border_width=1)
        self.copy_button.configure(command=self.copy)
        self.paste_button = ctk.CTkButton(master=self, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Paste", font=("Arial", 50, "bold"), border_width=1)
        self.paste_button.configure(command=self.paste)
        self.e_collapse = None

        self.undo_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="←Undo", font=("Arial", 50, "bold"), border_width=1)
        self.undo_button.configure(command=self.undo)
        self.undo_button.place(anchor="w", relx=0.2, rely=0.5)
        self.redo_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Redo→", font=("Arial", 50, "bold"), border_width=1)
        self.redo_button.configure(command=self.redo)
        self.redo_button.place(anchor="w", relx=0.3111, rely=0.5)
        self.raise_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="↑ Raise", font=("Arial", 50, "bold"), border_width=1)
        self.raise_button.configure(command=self.raise_element)
        self.raise_button.place(anchor="w", relx=0.42, rely=0.5)
        self.back_button = ctk.CTkButton(master=self.util_frame, width=width*0.1, height=height*0.095, fg_color=bg_color, text="Main Menu", font=("Arial", 50, "bold"), border_width=1)
        self.back_button.configure(command=self.destruct)
        self.back_button.place(anchor="e", relx=1, rely=0.5)

        self.tool_frame = ctk.CTkFrame(master=self, width=width, height=height*0.18, fg_color=bg_color, border_width=2)
        self.tool_frame.place(anchor="n", relx=0.5, rely=0.1)

        self.drawing_frame = ctk.CTkFrame(master=self, width=width, height=height*0.72, fg_color=bg_color, border_width=2)
        self.drawing_frame.place(anchor="n", relx=0.5, rely=0.28)
    
    def file_expand(self) -> None:
        self.file_button.configure(command=lambda e=None : self.file_collapse(e))
        self.new_button.place(anchor="w", relx=0, rely=0.145)
        self.new_button.tkraise()
        self.open_button.place(anchor="w", relx=0, rely=0.24)
        self.open_button.tkraise()
        self.save_button.place(anchor="w", relx=0, rely=0.335)
        self.save_button.tkraise()
        self.saveas_button.place(anchor="w", relx=0, rely=0.43)
        self.saveas_button.tkraise()
        self.f_collapse = self.window.bind("<Button-1>", self.file_collapse)

    def file_collapse(self, event) -> None:
        self.window.unbind("<Button-1>", self.f_collapse)
        if event:
            if event.widget not in (self.new_button, self.open_button, self.save_button, self.saveas_button):
                self.file_button.configure(command=self.file_expand)
                self.new_button.place_forget()
                self.open_button.place_forget()
                self.save_button.place_forget()
                self.saveas_button.place_forget()
        else:
            self.file_button.configure(command=self.file_expand)
            self.new_button.place_forget()
            self.open_button.place_forget()
            self.save_button.place_forget()
            self.saveas_button.place_forget()
        self.f_collapse = None

    def edit_expand(self) -> None:
        self.edit_button.configure(command=lambda e=None : self.edit_collapse(e))
        self.cut_button.place(anchor="w", relx=0.1, rely=0.145)
        self.cut_button.tkraise()
        self.copy_button.place(anchor="w", relx=0.1, rely=0.24)
        self.copy_button.tkraise()
        self.paste_button.place(anchor="w", relx=0.1, rely=0.335)
        self.paste_button.tkraise()
        self.e_collapse = self.window.bind("<Button-1>", self.edit_collapse)

    def edit_collapse(self, event) -> None:
        self.window.unbind("<Button-1>", self.e_collapse)
        if event:
            if event.widget not in (self.cut_button, self.copy_button, self.paste_button):
                self.edit_button.configure(command=self.edit_expand)
                self.cut_button.place_forget()
                self.copy_button.place_forget()
                self.paste_button.place_forget()
        else:
            self.edit_button.configure(command=self.edit_expand)
            self.cut_button.place_forget()
            self.copy_button.place_forget()
            self.paste_button.place_forget()
        self.e_collapse = None

    def new_project(self) -> None:
        if self.just_saved:
            for widget in self.drawing_frame.winfo_children():
                widget.destroy()
            self.just_saved = False

    def open_project(self) -> None:
        sample_element = Element(typ="label", relx=0.5, rely=0.5, window=self.drawing_frame)
        sample_element.place()
        self.project.add_element(sample_element)
        ...
        self.just_saved = True

    def save(self) -> None:
        if self.project.name == "":
            self.save_as()
            return

        data:dict = {}
        file_dir = rf"{constants.USERDATADIR}{gv.name}.json"
        project_data = []
        for proj in gv.user_projects:
            project_data.append(proj.as_dict())

        data = {
            gv.name: {
                "username": gv.username,
                "password": gv.password
            },
            "projects": project_data
        }

        try:
            os.remove(file_dir)
        except FileNotFoundError:
            pass
        
        with open(file_dir, "w") as file:
            json.dump(data, file, indent=4)

    def save_as(self) -> None:
        name = simpledialog.askstring("Project Name", "Please enter a project name:")
        elements = self.project.elements
        if name:
            self.project = None
            self.project = Project(name, elements)
        else:
            messagebox.showwarning("Input Error", "No project name entered.")
        self.save()

    def cut(self) -> None:
        ...
        self.just_saved = False
    
    def copy(self) -> None:
        ...
        self.just_saved = False
    
    def paste(self) -> None:
        ...
        self.just_saved = False

    def undo(self) -> None:
        ...
        self.just_saved = False

    def redo(self) -> None:
        ...
        self.just_saved = False

    def raise_element(self, element) -> None:
        ...
        self.just_saved = False

    def select(self) -> None:
        ...
    
    def select_elements(self) -> None:
        ...

    def select_all(self) -> None:
        ...

    def pencil(self) -> None:
        ...
        self.just_saved = False
    
    def erase(self) -> None:
        ...
        self.just_saved = False
    
    def change_draw_size(self) -> None:
        ...
    
    def fill(self) -> None:
        ...
        self.just_saved = False
    
    def eyedrop(self) -> None:
        ...

    def insert_text(self) -> None:
        ...
        self.just_saved = False

    def select_element(self) -> None:
        ...
    
    def place_element(self) -> None:
        ...
        self.just_saved = False
    
    def resize_element(self) -> None:
        ...
        self.just_saved = False
    
    def rotate_element(self) -> None:
        ...
        self.just_saved = False

    def select_color(self) -> None:
        ...
    
    def pick_color(self) -> None:
        ...

    def destruct(self) -> None:
        self.just_saved = True
        self.destroy()

    def change_proj(self, new_project:Project) -> None:
        self.project = new_project