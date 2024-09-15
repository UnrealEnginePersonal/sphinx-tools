import os as real_os
import shutil
from enum import Enum
from os import path as ospath


class SlashType(Enum):
    forward = '/'
    backward = '\\'


default_slash: SlashType = SlashType.forward

def remove_dir(path: str) -> None:
    """
    Remove a directory if it exists

    Args:
        path (str): The path to the directory to remove

    Returns:
        None
    """
    if real_os.path.exists(path):
        shutil.rmtree(path)


def recreate_dir(path: str) -> None:
    """
    Recreate a directory if it exists, otherwise create it

    Args:
        path (str): The path to the directory to (re)create

    Returns:
        None
    """
    if real_os.path.exists(path):
        shutil.rmtree(path)

    real_os.makedirs(path)


def join(__a: str, *paths: str, slash: SlashType = default_slash) -> str:
    result: str = ospath.join(__a, *paths)

    if slash == SlashType.backward:
        result = result.replace('/', '\\')
    else:
        result = result.replace('\\', '/')

    return result


def abspath(__a: str, slash: SlashType = default_slash) -> str:
    result: str = ospath.abspath(__a)

    if slash == SlashType.backward:
        result = result.replace('/', '\\')
    else:
        result = result.replace('\\', '/')

    return result


def exists(project_root: str) -> bool:
    return ospath.exists(project_root)


def isdir(project_root: str) -> bool:
    return ospath.isdir(project_root)
