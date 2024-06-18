from project import ProjectContainer, Project
import globalvariables as gv
import constants
import json
import os

def update_user_projects():
    data:dict = {}
    file_dir = rf"{constants.USERDATADIR}{gv.name}.json"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    gv.user_projects.clear()
    for idx, proj in enumerate(data["projects"]):
        proj_name = str(proj.keys())[12:-3]
        gv.user_projects.append(Project(name=proj_name))
        gv.user_projects[idx].build_elements(data["projects"][idx][proj_name]["elements"])

def load_project(projectname:str) -> None:
    proj_idx = -1
    for idx, proj in enumerate(gv.user_projects):
        if proj.name == projectname:
            proj_idx = idx
            break
    if proj_idx == -1:
        return
    
    data:dict = {}
    file_dir = rf"{constants.USERDATADIR}{gv.name}.json"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    desired_project = data["projects"][proj_idx][projectname]
    name = desired_project["name"]
    elements = desired_project["elements"]
    
    gv.curr_project = Project(name)
    gv.proj_container = ProjectContainer(
        window=gv.window,
        width=constants.WIDTH,
        height=constants.HEIGHT,
        project=gv.curr_project
    )
    gv.curr_project.build_and_place(gv.proj_container.drawing_frame, elements)
    
def save_project() -> None:
    data:dict = {}
    file_dir = constants.USER_PROJECTS_PATH + rf"{gv.project.name}.json"
    project_data = []
    for proj in gv.user_projects:
        project_data.append({proj.name: proj.as_dict()})

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