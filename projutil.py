import globalvariables as gv
import constants
import json
import os

def load_project(filename:str, projectname:str) -> None:
    data:dict = {}
    file_dir = rf"{filename}"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    gv.user_projects.clear()
    names = []
    for proj in data["projects"]:
        key = proj.keys()
        names.append(key)
        if projectname == key:
            gv.curr_project = proj[key]
    gv.user_projects = names.copy()

def save_project() -> None:
    data:dict = {}
    file_dir = constants.USER_PROJECTS_PATH + rf"\{gv.project.name}.json"
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