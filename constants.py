import os

PUBLICDIR = r"C:\Users\Public\Desktop"
HOMEDIR = os.getcwd()
USERDATADIR = HOMEDIR + r"\UserData\\"

WIDTH = 1734
HEIGHT = 975


def rgb_to_hex(rgb:tuple) -> str:
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

MAROON = rgb_to_hex((71, 0, 0))