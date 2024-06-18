from project import Project, ProjectContainer
import customtkinter as ctk
import constants

window = ctk.CTk(constants.MAROON)

name:str
username:str
password:str

user_projects:list[Project] = []
curr_project:Project = None
proj_container:ProjectContainer = None