from project import Project, ProjectContainer
from projbox import ProjBox
import customtkinter as ctk
import constants

window = ctk.CTk(constants.MAROON)

name:str
username:str
password:str

projbox:ProjBox

user_projects:list[Project] = []
curr_project:Project = None
proj_container:ProjectContainer = None