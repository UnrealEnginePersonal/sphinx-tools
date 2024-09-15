from typing import List
import glob

from  sphinx_tools.doxygen.models.module import Module
from sphinx_tools.doxygen.utils import path as path_utils

def find_modules(plugin_path: str) -> List[Module]:
    path_utils.abspath(plugin_path)
    project_root: str = path_utils.abspath(plugin_path)

    if not path_utils.exists(project_root):
        raise FileNotFoundError(f'Project root {project_root} does not exist')

    if not path_utils.isdir(project_root):
        raise NotADirectoryError(f'Project root {project_root} is not a directory')

    if project_root.endswith('Source'):
        project_root: str = path_utils.abspath(path_utils.join(project_root, '..'))

    src: str = path_utils.join(project_root, 'Source')

    for path in glob.iglob(f'{src}/**/Public', recursive=True):
        path: str = path.replace('\\', '/')

        module_source_path: str = path_utils.abspath(path_utils.join(path, '..'))

        frags: List[str] = path.split('/')
        name: str = frags[-2]
        cat: List[str] = frags[:-3]

        # remove all from cat except the last val
        cat = cat[-1:]

        yield Module(name=name,
                     cat=cat,
                     path=path,
                     sources=
                     [
                         path_utils.join(module_source_path, 'Public'),
                         path_utils.join(module_source_path, 'Private')
                     ])
