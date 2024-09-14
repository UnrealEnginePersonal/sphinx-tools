from enum import Enum
from os import path as ospath

class SlashType(Enum):
    forward = '/'
    backward = '\\'

default_slash: SlashType = SlashType.forward

def join(__a: str, *paths: str, slash:SlashType = default_slash) -> str:
    result:str = ospath.join(__a, *paths)

    if slash == SlashType.backward:
        result = result.replace('/', '\\')
    else:
        result = result.replace('\\', '/')

    return result


def abspath(__a: str, slash:SlashType = default_slash) -> str:
    result:str = ospath.abspath(__a)

    if slash == SlashType.backward:
        result = result.replace('/', '\\')
    else:
        result = result.replace('\\', '/')

    return result


def exists(project_root: str) -> bool:
    return ospath.exists(project_root)


def isdir(project_root: str) -> bool:
    return ospath.isdir(project_root)