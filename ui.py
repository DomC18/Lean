from fileutil import verify_existing
from screeninfo import get_monitors
from tkinter import messagebox
import globalvariables as gv
import customtkinter as ctk
from projbox import ProjBox 
from project import ProjectContainer, Project
import constants
import projutil

def destroy_children() -> None:
    try:
        for widget in gv.window.winfo_children():
            widget.destroy()
    except: pass

def init_window() -> None:
    gv.window.title("Lean")
    gv.window.resizable(width=False, height=False)
    horiz_offset = (get_monitors()[0].width - constants.WIDTH) / 2
    vert_offset = (get_monitors()[0].height - constants.HEIGHT) / 2
    gv.window.geometry(f"{constants.WIDTH}x{constants.HEIGHT}+{int(horiz_offset)}+{int(vert_offset)}")

def login_screen() -> None:
    destroy_children()

    gv.name = ""
    gv.username = ""
    gv.password = ""

    logo_label = ctk.CTkLabel(gv.window, text="Lean Login", font=("Arial", 120, "bold"), bg_color=constants.MAROON, width=1200, height=150)
    logo_label.place(relx=0.5, rely=0, anchor="n")
    firstname_label = ctk.CTkLabel(gv.window, text="*First Name:", font=("Arial", 100, "bold"), bg_color=constants.MAROON, width=100, height=100)
    firstname_label.place(relx=0.485, rely=0.325, anchor="e")
    firstname_entry = ctk.CTkEntry(gv.window, font=("Arial", 100), width=600, height=165)
    firstname_entry.place(relx=0.515, rely=0.325, anchor="w")
    username_label = ctk.CTkLabel(gv.window, text="*Username:", font=("Arial", 100, "bold"), bg_color=constants.MAROON, width=100, height=100)
    username_label.place(relx=0.485, rely=0.5, anchor="e")
    username_entry = ctk.CTkEntry(gv.window, font=("Arial", 100), width=600, height=165)
    username_entry.place(relx=0.515, rely=0.5, anchor="w")
    password_label = ctk.CTkLabel(gv.window, text="*Password:", font=("Arial", 100, "bold"), bg_color=constants.MAROON, width=100, height=100)
    password_label.place(relx=0.485, rely=0.675, anchor="e")
    password_entry = ctk.CTkEntry(gv.window, font=("Arial", 100), width=600, height=165)
    password_entry.place(relx=0.515, rely=0.675, anchor="w")
    login_button = ctk.CTkButton(gv.window, text="Login/Register", font=("Arial", 90, "bold"), width=15, height=75, command=lambda r=gv.window, f=firstname_entry, u=username_entry, p=password_entry, fl=firstname_label, ul=username_label, pl=password_label, func=project_select : verify_existing(r,f,u,p,fl,ul,pl,func))
    login_button.place(relx=0.5, rely=0.95, anchor="s")

    def exit(event) -> None:
        gv.window.destroy()

    gv.window.bind("<Escape>", exit)
    gv.window.mainloop()

def project_select() -> None:
    destroy_children()
    
    back_button = ctk.CTkButton(gv.window, text="← Back to Login", font=("Arial", 40, "bold"))
    back_button.configure(command=login_screen)
    back_button.place(relx=0.0001*9, rely=0.0001*16, anchor="nw")
    new_project_button = ctk.CTkButton(gv.window, text="New Project", font=("Arial", 90, "bold"))
    new_project_button.configure(command=new_project)
    new_project_button.place(relx=0.5, rely=0.33, anchor="center")
    old_project_button = ctk.CTkButton(gv.window, text="Old Project", font=("Arial", 90, "bold"))
    old_project_button.configure(command=lambda b=back_button, n=new_project_button, o=old_project_button : choose_project(b,n,o))
    old_project_button.place(relx=0.5, rely=0.66, anchor="center")

def choose_project(b:ctk.CTkButton, n:ctk.CTkButton, o:ctk.CTkButton) -> None:
    projutil.update_user_projects()
    if len(gv.user_projects) == 0:
        messagebox.showerror("Error", "No projects found")
        return

    boxframe = ctk.CTkFrame(gv.window, width=1500, height=800)
    boxframe.place(anchor="s", relx=0.5, rely=1)
    gv.projbox = ProjBox(master=boxframe, root=gv.window, width=1500, height=800, bg=constants.MAROON)
    gv.projbox.list_index = 0
    for idx, proj in enumerate(gv.user_projects):
        if idx < gv.projbox.list_index:
            continue
        if idx > gv.projbox.list_index + 6:
            break
        gv.projbox.insert(idx-gv.projbox.list_index, proj)
    gv.projbox.pack()
    up_button = ctk.CTkButton(boxframe, text="↑", bg_color=constants.MAROON, fg_color="black", font=("Arial", 46, "bold"), height=150)
    up_button.configure(command=gv.projbox.move_up)
    up_button.place(relx=1-(0.0001*16), rely=0+(0.0001*9), anchor="ne")
    down_button = ctk.CTkButton(boxframe, text="↓", bg_color=constants.MAROON, fg_color="black", font=("Arial", 46, "bold"), height=150)
    down_button.configure(command=gv.projbox.move_down)
    down_button.place(relx=1-(0.0001*16), rely=1-(0.0001*9), anchor="se")
    
    n.place_forget()
    o.place_forget()
    b.configure(command=project_select, text="← Project Select")
    b.place(relx=0.0001*9, rely=0.0001*16, anchor="nw")
    b.tkraise()    

def new_project() -> None:
    projutil.update_user_projects()
    gv.user_projects.append(Project())
    gv.curr_project = gv.user_projects[-1]
    gv.proj_container = None
    gv.proj_container = ProjectContainer(window=gv.window, projects=gv.user_projects, proj_idx=-1)
    gv.proj_container.place(anchor="center", relx=0.5, rely=0.5)