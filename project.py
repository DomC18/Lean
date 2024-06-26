from screeninfo import get_monitors
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
    def __init__(self, name:str="", elements:list[Element]=None) -> None:
        self.name = name
        if not elements:
            self.elements = []
        else:
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
    def __init__(self, window:ctk.CTk, width=constants.WIDTH, height=constants.HEIGHT, bg_color=constants.MAROON, projects:list=[], proj_idx:int=-1, **kwargs) -> None:
        super().__init__(master=window, width=width, height=height, bg_color=bg_color, **kwargs)
        self.window = window
        self.projects = projects
        self.proj_idx = proj_idx
        self.bg_color = bg_color

        self.shape_dict = {
            "line": 0,#ctk.CTkImage(),
            "circle": 1,#ctk.CTkImage(),
            "rectangle": 2,#ctk.CTkImage(),
            "roundedrectangle": 3,#ctk.CTkImage(),
            "triangle": 4,#ctk.CTkImage(),
            "righttriangle": 5,#ctk.CTkImage(),
            "diamond": 6,#ctk.CTkImage(),
            "pentagon": 7,#ctk.CTkImage(),
            "hexagon": 8,#ctk.CTkImage(),
            "rightarrow": 9,#ctk.CTkImage(),
            "leftarrow": 10,#ctk.CTkImage(),
            "uparrow": 11,#ctk.CTkImage(),
            "downarrow": 12,#ctk.CTkImage(),
            "fourpointstar": 13,#ctk.CTkImage(),
            "fivepointstar": 14,#ctk.CTkImage(),
            "array": 15,#ctk.CTkImage(),
            "twodimensionalarray": 16,#ctk.CTkImage(),
            "singlylinkedlist": 17,#ctk.CTkImage(),
            "doublylinkedlist": 18,#ctk.CTkImage(),
            "stack": 19,#ctk.CTkImage(),
            "queue": 20,#ctk.CTkImage(),
            "binarytree": 21,#ctk.CTkImage(),
            "heap": 22,#ctk.CTkImage(),
            "hashtable": 23,#ctk.CTkImage(),
            "graph": 24#ctk.CTkImage()
        }

        self.func_dict = {
            "select": [self.select_tool_start,self.select_tool_during,self.select_tool_end],
            "pencil": [self.pencil_tool_start,self.pencil_tool_during,self.pencil_tool_end],
            "erase": [self.erase_tool_start,self.erase_tool_during,self.erase_tool_end],
            "text": [self.text_tool_start,self.text_tool_during,self.text_tool_end],
            "line": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "circle": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "rectangle": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "roundedrectangle": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "triangle": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "righttriangle": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "diamond": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "pentagon": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "hexagon": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "rightarrow": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "leftarrow": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "uparrow": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "downarrow": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "fourpointstar": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "fivepointstar": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "array": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "twodimensionalarray": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "singlylinkedlist": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "doublylinkedlist": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "stack": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "queue": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "binarytree": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "heap": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "hashtable": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end],
            "graph": [self.shape_tool_start,self.shape_tool_during,self.shape_tool_end]
        }

        self.mouse_held = False
        self.enter_held = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_widget = None
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.curr_x = 0
        self.curr_y = 0
        self.prev_x = 0
        self.prev_y = 0
        self.select_box_width = 0
        self.select_box_height = 0
        self.shape_box_width = 0
        self.shape_box_height = 0
        self.prev_length = 0
        self.text_length = 16
        self.text_size = 28
        self.text_boxes = []
        self.curr_entry = None
        self.entry_placed = False

        self.started_tool = False
        self.curr_tool = "pencil"
        self.curr_tool_selected = None
        self.curr_color = "black"
        self.curr_color_selected = None
        self.curr_shape = None

        self.util_frame = ctk.CTkFrame(master=self, width=width, height=height*0.1, fg_color=bg_color, border_width=3)
        self.util_frame.place(anchor="n", relx=0.5, rely=0)
        self.mass_frame = ctk.CTkFrame(master=self, width=width, height=height*0.18, fg_color=bg_color, border_width=3)
        self.mass_frame.place(anchor="n", relx=0.5, rely=0.1)
        self.drawing_frame = ctk.CTkFrame(master=self, width=width, height=height*0.72, fg_color=bg_color, border_width=3)
        self.drawing_frame.place(anchor="n", relx=0.5, rely=0.28)
        self.drawing_canvas = ctk.CTkCanvas(master=self.drawing_frame, width=width, height=height*0.72, bg=bg_color)
        self.drawing_canvas.place(anchor="center", relx=0.5, rely=0.5)
        self.select_box = ctk.CTkLabel(master=self.drawing_canvas, text="", corner_radius=1, fg_color=constants.DARKMAROON)
        self.shape_box = ctk.CTkLabel(master=self.drawing_canvas, text="", corner_radius=1, fg_color=constants.DARKMAROON)

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

        self.tool_frame = ctk.CTkFrame(master=self.mass_frame, width=width*0.25, height=height*0.1795, fg_color=bg_color, border_width=3)
        self.tool_frame.place(anchor="center", relx=0.125, rely=0.5)
        self.select_button = ctk.CTkButton(master=self.tool_frame, width=width*0.22*0.5, height=height*0.15*0.33, fg_color=bg_color, border_width=1, text="Select", border_color="black")
        self.select_button.configure(command=lambda t="select", b=self.select_button : self.choose_tool(t,b))
        self.select_button.place(anchor="center", relx=0.25, rely=1/6)
        self.pencil_button = ctk.CTkButton(master=self.tool_frame, width=width*0.22*0.5, height=height*0.15*0.33, fg_color=bg_color, border_width=1, text="Pencil", border_color="black")
        self.pencil_button.configure(command=lambda t="pencil", b=self.pencil_button : self.choose_tool(t,b))
        self.pencil_button.place(anchor="center", relx=0.25, rely=3/6)
        self.erase_button = ctk.CTkButton(master=self.tool_frame, width=width*0.22*0.5, height=height*0.15*0.33, fg_color=bg_color, border_width=1, text="Erase", border_color="black")
        self.erase_button.configure(command=lambda t="erase", b=self.erase_button : self.choose_tool(t,b))
        self.erase_button.place(anchor="center", relx=0.25, rely=5/6)
        self.text_button = ctk.CTkButton(master=self.tool_frame, width=width*0.22*0.5, height=height*0.15*0.33, fg_color=bg_color, border_width=1, text="Text", border_color="black")
        self.text_button.configure(command=lambda t="text", b=self.text_button : self.choose_tool(t,b))
        self.text_button.place(anchor="center", relx=0.75, rely=1/6)
        self.choose_tool(tool="pencil", button=self.pencil_button)

        self.color_frame = ctk.CTkFrame(master=self.mass_frame, width=width*0.25, height=height*0.1795, fg_color=bg_color, border_width=3)
        self.color_frame.place(anchor="center", relx=0.375, rely=0.5)
        self.black_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#000000", border_width=1, text="", border_color="black")
        self.black_color_button.configure(command=lambda c="#000000", b=self.black_color_button: self.choose_color(c, b))
        self.black_color_button.place(anchor="center", relx=0.1, rely=0.125)
        self.white_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#ffffff", border_width=1, text="", border_color="black")
        self.white_color_button.configure(command=lambda c="#ffffff", b=self.white_color_button: self.choose_color(c, b))
        self.white_color_button.place(anchor="center", relx=0.1, rely=0.375)
        self.gray_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#808080", border_width=1, text="", border_color="black")
        self.gray_color_button.configure(command=lambda c="#808080", b=self.gray_color_button: self.choose_color(c, b))
        self.gray_color_button.place(anchor="center", relx=0.1, rely=0.625)
        self.lightgray_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#c0c0c0", border_width=1, text="", border_color="black")
        self.lightgray_color_button.configure(command=lambda c="#c0c0c0", b=self.lightgray_color_button: self.choose_color(c, b))
        self.lightgray_color_button.place(anchor="center", relx=0.1, rely=0.875)
        self.darkred_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#8b0000", border_width=1, text="", border_color="black")
        self.darkred_color_button.configure(command=lambda c="#8b0000", b=self.darkred_color_button: self.choose_color(c, b))
        self.darkred_color_button.place(anchor="center", relx=0.3, rely=0.125)
        self.maroon_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color=constants.MAROON, border_width=1, text="", border_color="black")
        self.maroon_color_button.configure(command=lambda c=constants.MAROON, b=self.maroon_color_button: self.choose_color(c, b))
        self.maroon_color_button.place(anchor="center", relx=0.3, rely=0.375)
        self.red_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#ff0000", border_width=1, text="", border_color="black")
        self.red_color_button.configure(command=lambda c="#ff0000", b=self.red_color_button: self.choose_color(c, b))
        self.red_color_button.place(anchor="center", relx=0.3, rely=0.625)
        self.rose_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#f08080", border_width=1, text="", border_color="black")
        self.rose_color_button.configure(command=lambda c="#f08080", b=self.rose_color_button: self.choose_color(c, b))
        self.rose_color_button.place(anchor="center", relx=0.3, rely=0.875)
        self.orange_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#ffa500", border_width=1, text="", border_color="black")
        self.orange_color_button.configure(command=lambda c="#ffa500", b=self.orange_color_button: self.choose_color(c, b))
        self.orange_color_button.place(anchor="center", relx=0.5, rely=0.125)
        self.gold_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#ffd700", border_width=1, text="", border_color="black")
        self.gold_color_button.configure(command=lambda c="#ffd700", b=self.gold_color_button: self.choose_color(c, b))
        self.gold_color_button.place(anchor="center", relx=0.5, rely=0.375)
        self.yellow_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#ffff00", border_width=1, text="", border_color="black")
        self.yellow_color_button.configure(command=lambda c="#ffff00", b=self.yellow_color_button: self.choose_color(c, b))
        self.yellow_color_button.place(anchor="center", relx=0.5, rely=0.625)
        self.cream_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#fffdd0", border_width=1, text="", border_color="black")
        self.cream_color_button.configure(command=lambda c="#fffdd0", b=self.cream_color_button: self.choose_color(c, b))
        self.cream_color_button.place(anchor="center", relx=0.5, rely=0.875)
        self.green_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#008000", border_width=1, text="", border_color="black")
        self.green_color_button.configure(command=lambda c="#008000", b=self.green_color_button: self.choose_color(c, b))
        self.green_color_button.place(anchor="center", relx=0.7, rely=0.125)
        self.limegreen_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#90ee90", border_width=1, text="", border_color="black")
        self.limegreen_color_button.configure(command=lambda c="#90ee90", b=self.limegreen_color_button: self.choose_color(c, b))
        self.limegreen_color_button.place(anchor="center", relx=0.7, rely=0.375)
        self.blue_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#0000ff", border_width=1, text="", border_color="black")
        self.blue_color_button.configure(command=lambda c="#0000ff", b=self.blue_color_button: self.choose_color(c, b))
        self.blue_color_button.place(anchor="center", relx=0.7, rely=0.625)
        self.cyan_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#00ffff", border_width=1, text="", border_color="black")
        self.cyan_color_button.configure(command=lambda c="#00ffff", b=self.cyan_color_button: self.choose_color(c, b))
        self.cyan_color_button.place(anchor="center", relx=0.7, rely=0.875)
        self.turquoise_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#00ced1", border_width=1, text="", border_color="black")
        self.turquoise_color_button.configure(command=lambda c="#00ced1", b=self.turquoise_color_button: self.choose_color(c, b))
        self.turquoise_color_button.place(anchor="center", relx=0.9, rely=0.125)
        self.navy_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#000080", border_width=1, text="", border_color="black")
        self.navy_color_button.configure(command=lambda c="#000080", b=self.navy_color_button: self.choose_color(c, b))
        self.navy_color_button.place(anchor="center", relx=0.9, rely=0.375)
        self.purple_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#800080", border_width=1, text="", border_color="black")
        self.purple_color_button.configure(command=lambda c="#800080", b=self.purple_color_button: self.choose_color(c, b))
        self.purple_color_button.place(anchor="center", relx=0.9, rely=0.625)
        self.magenta_color_button = ctk.CTkButton(master=self.color_frame, width=int(width*0.25*0.2*0.5), height=int(height*0.1795*0.25*0.75), fg_color="#ff00ff", border_width=1, text="", border_color="black")
        self.magenta_color_button.configure(command=lambda c="#ff00ff", b=self.magenta_color_button: self.choose_color(c, b))
        self.magenta_color_button.place(anchor="center", relx=0.9, rely=0.875)
        self.choose_color(color="black", button=self.black_color_button)

        self.shapes_frame = ctk.CTkFrame(master=self.mass_frame, width=width*0.25, height=height*0.1795, fg_color=bg_color, border_width=3)
        self.shapes_frame.place(anchor="center", relx=0.625, rely=0.5)
        self.line_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="ln", border_color="black")
        self.line_button.configure(command=lambda t="line", b=self.line_button : self.choose_tool(t,b))
        self.line_button.place(anchor="center", relx=0.125, rely=0.125)
        self.circle_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="cr", border_color="black")
        self.circle_button.configure(command=lambda t="circle", b=self.circle_button : self.choose_tool(t,b))
        self.circle_button.place(anchor="center", relx=0.375, rely=0.125)
        self.rectangle_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="re", border_color="black")
        self.rectangle_button.configure(command=lambda t="rectangle", b=self.rectangle_button : self.choose_tool(t,b))
        self.rectangle_button.place(anchor="center", relx=0.625, rely=0.125)
        self.roundedrectangle_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="rr", border_color="black")
        self.roundedrectangle_button.configure(command=lambda t="roundedrectangle", b=self.roundedrectangle_button : self.choose_tool(t,b))
        self.roundedrectangle_button.place(anchor="center", relx=0.875, rely=0.125)
        self.triangle_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="tr", border_color="black")
        self.triangle_button.configure(command=lambda t="triangle", b=self.triangle_button : self.choose_tool(t,b))
        self.triangle_button.place(anchor="center", relx=0.125, rely=0.375)
        self.righttriangle_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="rt", border_color="black")
        self.righttriangle_button.configure(command=lambda t="righttriangle", b=self.righttriangle_button : self.choose_tool(t,b))
        self.righttriangle_button.place(anchor="center", relx=0.375, rely=0.375)
        self.diamond_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="di", border_color="black")
        self.diamond_button.configure(command=lambda t="diamond", b=self.diamond_button : self.choose_tool(t,b))
        self.diamond_button.place(anchor="center", relx=0.625, rely=0.375)
        self.pentagon_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="pt", border_color="black")
        self.pentagon_button.configure(command=lambda t="pentagon", b=self.pentagon_button : self.choose_tool(t,b))
        self.pentagon_button.place(anchor="center", relx=0.875, rely=0.375)
        self.hexagon_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="hx", border_color="black")
        self.hexagon_button.configure(command=lambda t="hexagon", b=self.hexagon_button : self.choose_tool(t,b))
        self.hexagon_button.place(anchor="center", relx=0.125, rely=0.625)
        self.rightarrow_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="ra", border_color="black")
        self.rightarrow_button.configure(command=lambda t="rightarrow", b=self.rightarrow_button : self.choose_tool(t,b))
        self.rightarrow_button.place(anchor="center", relx=0.375, rely=0.625)
        self.leftarrow_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="la", border_color="black")
        self.leftarrow_button.configure(command=lambda t="leftarrow", b=self.leftarrow_button : self.choose_tool(t,b))
        self.leftarrow_button.place(anchor="center", relx=0.625, rely=0.625)
        self.uparrow_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="ua", border_color="black")
        self.uparrow_button.configure(command=lambda t="uparrow", b=self.uparrow_button : self.choose_tool(t,b))
        self.uparrow_button.place(anchor="center", relx=0.875, rely=0.625)
        self.downarrow_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="da", border_color="black")
        self.downarrow_button.configure(command=lambda t="downarrow", b=self.downarrow_button : self.choose_tool(t,b))
        self.downarrow_button.place(anchor="center", relx=0.125, rely=0.875)
        self.fourpointstar_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="4s", border_color="black")
        self.fourpointstar_button.configure(command=lambda t="fourpointstar", b=self.fourpointstar_button : self.choose_tool(t,b))
        self.fourpointstar_button.place(anchor="center", relx=0.375, rely=0.875)
        self.fivepointstar_button = ctk.CTkButton(master=self.shapes_frame, width=width*0.22*0.25, height=height*0.15*0.25, fg_color=bg_color, border_width=1, text="5s", border_color="black")
        self.fivepointstar_button.configure(command=lambda t="fivepointstar", b=self.fivepointstar_button : self.choose_tool(t,b))
        self.fivepointstar_button.place(anchor="center", relx=0.625, rely=0.875)

        self.advshapes_frame = ctk.CTkFrame(master=self.mass_frame, width=width*0.25, height=height*0.1795, fg_color=bg_color, border_width=3)
        self.advshapes_frame.place(anchor="center", relx=0.875, rely=0.5)
        self.array_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="ar", border_color="black")
        self.array_button.configure(command=lambda t="array", b=self.array_button : self.choose_tool(t,b))
        self.array_button.place(anchor="center", relx=0.1, rely=0.25)
        self.twodimensionalarray_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="2r", border_color="black")
        self.twodimensionalarray_button.configure(command=lambda t="twodimensionalarray", b=self.twodimensionalarray_button : self.choose_tool(t,b))
        self.twodimensionalarray_button.place(anchor="center", relx=0.3, rely=0.25)
        self.singlylinkedlist_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="sl", border_color="black")
        self.singlylinkedlist_button.configure(command=lambda t="singlylinkedlist", b=self.singlylinkedlist_button : self.choose_tool(t,b))
        self.singlylinkedlist_button.place(anchor="center", relx=0.5, rely=0.25)
        self.doublylinkedlist_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="dl", border_color="black")
        self.doublylinkedlist_button.configure(command=lambda t="doublylinkedlist", b=self.doublylinkedlist_button : self.choose_tool(t,b))
        self.doublylinkedlist_button.place(anchor="center", relx=0.7, rely=0.25)
        self.stack_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="st", border_color="black")
        self.stack_button.configure(command=lambda t="stack", b=self.stack_button : self.choose_tool(t,b))
        self.stack_button.place(anchor="center", relx=0.9, rely=0.25)
        self.queue_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="qu", border_color="black")
        self.queue_button.configure(command=lambda t="queue", b=self.queue_button : self.choose_tool(t,b))
        self.queue_button.place(anchor="center", relx=0.1, rely=0.75)
        self.binarytree_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="bt", border_color="black")
        self.binarytree_button.configure(command=lambda t="binarytree", b=self.binarytree_button : self.choose_tool(t,b))
        self.binarytree_button.place(anchor="center", relx=0.3, rely=0.75)
        self.heap_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="hp", border_color="black")
        self.heap_button.configure(command=lambda t="heap", b=self.heap_button : self.choose_tool(t,b))
        self.heap_button.place(anchor="center", relx=0.5, rely=0.75)
        self.hashtable_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="ha", border_color="black")
        self.hashtable_button.configure(command=lambda t="hashtable", b=self.hashtable_button : self.choose_tool(t,b))
        self.hashtable_button.place(anchor="center", relx=0.7, rely=0.75)
        self.graph_button = ctk.CTkButton(master=self.advshapes_frame, width=width*0.22*0.2, height=height*0.15*0.5, fg_color=bg_color, border_width=1, text="gr", border_color="black")
        self.graph_button.configure(command=lambda t="graph", b=self.graph_button : self.choose_tool(t,b))
        self.graph_button.place(anchor="center", relx=0.9, rely=0.75)

        self.handling_id = self.window.after(20, self.handle_tool)
        self.window.bind("<ButtonPress-1>", self.mouse_clicked)
        self.window.bind("<ButtonRelease-1>", self.mouse_idle)
        self.window.bind("<B1-Motion>", self.mouse_clicked)
        self.window.bind('<Return>', self.enter_clicked)
        self.window.bind('<KeyRelease-Return>', self.enter_idle)
    
    def mouse_clicked(self, event) -> None: 
        self.mouse_held = True
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.mouse_widget = event.widget
    
    def mouse_idle(self, event) -> None:
        self.mouse_held = False
        self.mouse_x = event.x
        self.mouse_y = event.y

    def enter_clicked(self, event) -> None:
        self.enter_held = True
    
    def enter_idle(self, event) -> None:
        self.enter_held = False

    def handle_tool(self) -> None:
        try:
            self.start_handler = self.func_dict[self.curr_tool][0]
            self.during_handler = self.func_dict[self.curr_tool][1]
            self.end_handler = self.func_dict[self.curr_tool][2]
        except:
            return
    
        self.start_handler()
        self.window.after(20, self.handle_tool)

    def select_tool_start(self) -> None:
        if self.mouse_widget != self.drawing_canvas and self.mouse_widget not in self.drawing_canvas.winfo_children():
            return
        if not self.started_tool:
            if self.mouse_held:
                try:
                    self.select_box.place_forget()
                    self.select_box.configure(width=0, height=0)
                    self.shape_box.place_forget()
                    self.shape_box.configure(width=0, height=0)
                except: pass

                self.started_tool = True
                self.start_x = self.mouse_x
                self.start_y = self.mouse_y
            return
        self.select_tool_during()
    
    def select_tool_during(self) -> None:
        if self.mouse_held:
            self.end_x = self.mouse_x
            self.end_y = self.mouse_y
            
            self.select_box.place_forget()
            self.select_box_width = 0
            self.select_box_height = 0
            if self.end_x-self.start_x > 0:
                self.select_box_width = self.end_x-self.start_x
                if self.end_y-self.start_y > 0:
                    self.select_box_height = self.end_y-self.start_y
                    self.select_box.configure(width=self.select_box_width, height=self.select_box_height)
                    self.select_box.place(anchor="nw", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
                else:
                    self.select_box_height = self.start_y-self.end_y
                    self.select_box.configure(width=self.select_box_width, height=self.select_box_height)
                    self.select_box.place(anchor="sw", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
            else:
                self.select_box_width = self.start_x-self.end_x
                if self.end_y-self.start_y > 0:
                    self.select_box_height = self.end_y-self.start_y
                    self.select_box.configure(width=self.select_box_width, height=self.select_box_height)
                    self.select_box.place(anchor="ne", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
                else:
                    self.select_box_height = self.start_y-self.end_y
                    self.select_box.configure(width=self.select_box_width, height=self.select_box_height)
                    self.select_box.place(anchor="se", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
            return
        
        self.select_tool_end()
    
    def select_tool_end(self) -> None:
        self.started_tool = False
        self.start_x = 0
        self.start_y = 0

    def pencil_tool_start(self) -> None:
        if self.mouse_widget != self.drawing_canvas and self.mouse_widget not in self.drawing_canvas.winfo_children():
            return
        if not self.started_tool:
            if self.mouse_held:
                try:
                    self.select_box.place_forget()
                    self.select_box.configure(width=0, height=0)
                    self.shape_box.place_forget()
                    self.shape_box.configure(width=0, height=0)
                except: pass

                self.started_tool = True
                self.curr_x = self.mouse_x
                self.curr_y = self.mouse_y
            return
        self.pencil_tool_during()
    
    def pencil_tool_during(self) -> None:
        if self.mouse_held:
            if self.prev_x == 0 and self.prev_y == 0:
                self.prev_x = self.mouse_x
                self.prev_y = self.mouse_y
                return

            self.curr_x = self.mouse_x
            self.curr_y = self.mouse_y

            self.drawing_canvas.create_line(self.prev_x, self.prev_y, self.curr_x, self.curr_y, fill=self.curr_color, width=20)

            self.prev_x = self.curr_x
            self.prev_y = self.curr_y
            return        
        self.pencil_tool_end()
    
    def pencil_tool_end(self) -> None:
        self.started_tool = False
        self.curr_x = 0
        self.curr_y = 0
        self.prev_x = 0
        self.prev_y = 0
    
    def erase_tool_start(self) -> None:
        if self.mouse_widget != self.drawing_canvas and self.mouse_widget not in self.drawing_canvas.winfo_children():
            return
        if not self.started_tool:
            if self.mouse_held:
                try:
                    self.select_box.place_forget()
                    self.select_box.configure(width=0, height=0)
                    self.shape_box.place_forget()
                    self.shape_box.configure(width=0, height=0)
                except: pass

                self.started_tool = True
                self.curr_x = self.mouse_x
                self.curr_y = self.mouse_y
            return
        self.erase_tool_during()
    
    def erase_tool_during(self) -> None:
        if self.mouse_held:
            if self.prev_x == 0 and self.prev_y == 0:
                self.prev_x = self.mouse_x
                self.prev_y = self.mouse_y
                return

            self.curr_x = self.mouse_x
            self.curr_y = self.mouse_y

            self.drawing_canvas.create_line(self.prev_x, self.prev_y, self.curr_x, self.curr_y, fill=constants.MAROON, width=50)

            self.prev_x = self.curr_x
            self.prev_y = self.curr_y
            return
        self.erase_tool_end()
    
    def erase_tool_end(self) -> None:
        self.started_tool = False
        self.curr_x = 0
        self.curr_y = 0
        self.prev_x = 0
        self.prev_y = 0

    def text_tool_start(self) -> None:
        if self.mouse_widget != self.drawing_canvas and self.mouse_widget not in self.drawing_canvas.winfo_children():
            return
        if not self.started_tool:
            if self.mouse_held:
                try:
                    self.select_box.place_forget()
                    self.select_box.configure(width=0, height=0)
                    self.shape_box.place_forget()
                    self.shape_box.configure(width=0, height=0)
                except: pass

                self.started_tool = True
                self.start_x = self.mouse_x
                self.start_y = self.mouse_y
            return
        self.text_tool_during()
    
    def text_tool_during(self) -> None:
        if not self.enter_held:
            if not self.curr_entry:
                self.curr_entry = ctk.CTkEntry(master=self.drawing_canvas, width=self.text_length, height=40, font=("Times New Roman", self.text_size, "bold"))
                self.curr_entry.focus_set()
                self.prev_length = self.text_length
                return

            if len(self.curr_entry.get()) > 0:
                if len(self.curr_entry.get()) != self.prev_length:
                    self.curr_entry.configure(width=len(self.curr_entry.get())*self.text_length)
            elif len(self.curr_entry.get()) == 0 and self.prev_length != 0:
                self.curr_entry.configure(width=self.text_length)
            self.prev_length = len(self.curr_entry.get())
        
            if not self.entry_placed:
                self.curr_entry.place(anchor="center", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
                self.entry_placed = True
            return
        self.text_tool_end()

    def text_tool_end(self) -> None:
        self.new_label = ctk.CTkLabel(master=self.drawing_canvas, width=len(self.curr_entry.get())*self.text_length, height=40, font=("Times New Roman", self.text_size, "bold"), text=self.curr_entry.get())
        self.text_boxes.append(self.new_label)
        self.new_label.place(anchor="center", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
        self.curr_entry.destroy()

        self.curr_entry = None
        self.entry_placed = False
        self.started_tool = False
        self.prev_length = 0
        self.start_x = 0
        self.start_y = 0
    
    def shape_tool_start(self) -> None:
        self.curr_shape = self.shape_dict[self.curr_tool]
        if self.mouse_widget != self.drawing_canvas and self.mouse_widget not in self.drawing_canvas.winfo_children():
            return
        if not self.started_tool:
            if self.mouse_held:
                try:
                    self.select_box.place_forget()
                    self.select_box.configure(width=0, height=0)
                    self.shape_box.place_forget()
                    self.shape_box.configure(width=0, height=0)
                except: pass

                self.started_tool = True
                self.start_x = self.mouse_x
                self.start_y = self.mouse_y
            return
        self.shape_tool_during()
    
    def shape_tool_during(self) -> None:
        if self.mouse_held:
            self.end_x = self.mouse_x
            self.end_y = self.mouse_y
            
            self.shape_box.place_forget()
            self.shape_box_width = 0
            self.shape_box_height = 0
            if self.end_x-self.start_x > 0:
                self.shape_box_width = self.end_x-self.start_x
                if self.end_y-self.start_y > 0:
                    self.shape_box_height = self.end_y-self.start_y
                    self.shape_box.configure(width=self.shape_box_width, height=self.shape_box_height)
                    self.shape_box.place(anchor="nw", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
                else:
                    self.shape_box_height = self.start_y-self.end_y
                    self.shape_box.configure(width=self.shape_box_width, height=self.shape_box_height)
                    self.shape_box.place(anchor="sw", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
            else:
                self.shape_box_width = self.start_x-self.end_x
                if self.end_y-self.start_y > 0:
                    self.shape_box_height = self.end_y-self.start_y
                    self.shape_box.configure(width=self.shape_box_width, height=self.shape_box_height)
                    self.shape_box.place(anchor="ne", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
                else:
                    self.shape_box_height = self.start_y-self.end_y
                    self.shape_box.configure(width=self.shape_box_width, height=self.shape_box_height)
                    self.shape_box.place(anchor="se", relx=self.start_x/constants.WIDTH, rely=self.start_y/((1-0.2795)*constants.HEIGHT))
            return
        
        self.shape_tool_end()
    
    def shape_tool_end(self) -> None:
        ...

        self.started_tool = False
        self.curr_shape = None
        self.start_x = 0
        self.start_y = 0

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
        if not self.just_saved:
            self.save()
        
        self.projects.append(Project())
        self.proj_idx = -1

        for child in self.drawing_frame.winfo_children():
            child.destroy()
        
        self.just_saved = False

    def open_project(self) -> None:
        name_empty = self.projects[self.proj_idx].name == ""
        if not self.just_saved and not name_empty:
            self.save()

        if len(self.projects) <= 1:
            messagebox.showinfo("Number of Projects", "One or less projects are present on this account. Please create a new project.")
            return

        if name_empty:
            self.projects.pop()

        self.destruct()
        self.just_saved = False
        gv.projbox.list_index = 0

    def save(self) -> None:
        if self.projects[self.proj_idx].name == "":
            self.save_as()
            return

        data:dict = {}
        file_dir = rf"{constants.USERDATADIR}{gv.name}.json"
        project_data = []
        for proj in self.projects:
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
        
        self.just_saved = True

    def save_as(self) -> None:
        window = ctk.CTk(constants.MAROON)
        window.title("Save Project As")
        window.resizable(width=False, height=False)
        horiz_offset = (get_monitors()[0].width - int(constants.WIDTH/5)) / 2
        vert_offset = (get_monitors()[0].height - int(constants.HEIGHT/5)) / 2
        window.geometry(f"{int(constants.WIDTH/5)}x{int(constants.HEIGHT/5)}+{horiz_offset}+{vert_offset}")
        
        entry = ctk.CTkEntry(window, width=int(constants.WIDTH/7.5), font=("Times New Roman", 30, "bold"))
        entry.place(anchor="center", relx=0.5, rely=0.33)
        confirm = ctk.CTkButton(window, width=int(constants.WIDTH/7/5), font=("Times New Roman", 30, "bold"), text="Confirm Name")
        confirm.configure(command=lambda e=entry : validate_name(e))
        confirm.place(anchor="center", relx=0.5, rely=0.66)

        def validate_name(entry:ctk.CTkEntry) -> None:
            name = entry.get()
            if name != "":
                elements = self.projects[self.proj_idx].elements
                self.projects[self.proj_idx] = None; gv.user_projects[self.proj_idx] = None
                self.projects[self.proj_idx] = Project(name, elements); gv.user_projects[self.proj_idx] = Project(name, elements)
                window.destroy()
                self.save()
            else:
                messagebox.showwarning("Input Error", "No project name entered.")
                return
        
        window.mainloop()
            
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

    def choose_color(self, color:str, button:ctk.CTkButton) -> None:
        self.curr_color = color
        if self.curr_color_selected:
            self.curr_color_selected.configure(border_width=1)
        button.configure(border_width=5)
        self.curr_color_selected = button

    def choose_tool(self, tool:str, button:ctk.CTkButton) -> None:
        self.curr_tool = tool
        if self.curr_tool_selected:
            self.curr_tool_selected.configure(border_width=1)
        button.configure(border_width=5)
        self.curr_tool_selected = button
    
    def place_elements(self) -> None:
        for element in self.projects[self.proj_idx].elements:
            element.window = self.drawing_canvas
            element.apply_config()
            element.place()

    def destruct(self) -> None:
        self.destroy()
        self.window.after_cancel(self.handling_id)
        self.window.unbind_all()