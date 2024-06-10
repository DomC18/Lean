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
    names = []
    for proj in data["projects"]:
        key = str(proj.keys())[12:-3]
        names.append(key)
    gv.user_projects = names.copy()

def load_project(projectname:str) -> None:
    proj_idx = gv.user_projects.index(projectname)
    
    """
    desired_project = data["projects"][proj_idx][projectname]
    gv.curr_project = Project(
        desired_project[name],
        desired_project[desc],
        desired_project[etc],
    )
    elements = desired_project[elements]
    gv.curr_project.build_elements(gv.curr_project, elements)
    """
    
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