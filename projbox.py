import globalvariables as gv
import tkinter as tk
import projutil

class ProjBox(tk.Frame):
    def __init__(self, setup_func, master=None, root=tk.Tk, width=0, height=0, bg="white", **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg)
        self.bg_color = self.rgb_to_hex((240, 240, 240))
        self.list_frame = tk.Frame(self.canvas)
        self.setup_func = setup_func
        self.root = root
        self.bg = bg
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_index:int
        self.proj_combos = {}

    def rgb_to_hex(self, rgb:tuple) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def insert(self, idx:int, projname:str) -> None:
        y_multiplier = 0.00175+(idx*0.13875)        
        name_select = tk.Button(self.canvas, text=projname.casefold().capitalize(), font=('Arial', 50), bg=self.bg)
        name_select.configure(command=lambda p=projname : self.select_proj(p))
        name_select.place(relx=0.001, rely=y_multiplier, anchor="nw")

        self.proj_combos.update({projname:[projname, name_select]})
            
    def move_down(self) -> None:
        if self.list_index+8 > len(gv.user_projects):
            return

        self.list_index += 1
        self.insert_all()

    def move_up(self) -> None:
        if self.list_index <= 0:
            return
        
        self.list_index -= 1
        self.insert_all()

    def del_row_elements(self):
        proj_names = self.proj_combos.keys()

        for proj_name in proj_names:
            self.proj_combos[proj_name][1].destroy()

    def insert_all(self) -> None:
        self.del_row_elements()
        self.place_forget()

        for idx, proj in enumerate(gv.user_projects):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, proj)
        self.pack()
    
    def select_proj(self, proj_name:str):
        projutil.load_project(proj_name)
        self.setup_func()