import glob
from typing import List


import os.path as ospath
import sys

sys.path.append(ospath.abspath(ospath.join(ospath.dirname(__file__), '..')))

import utils.path
from models.plugin_model import PluginModel
from models.module import Module


def extract_category(frags: List[str], start_tag: str, end_tag: str) -> List[str]:
    cat: List[str] = []
    cat_started:bool = False

    for frag in frags:
        if frag == start_tag:
            cat_started = True
            continue

        if frag == end_tag:
            break

        if cat_started:
            cat.append(frag)

    return cat


def find_modules(project_root: str) -> List[Module]:
    project_root:str = utils.path.abspath(project_root)

    if not utils.path.exists(project_root):
        raise FileNotFoundError(f'Project root {project_root} does not exist')

    if not utils.path.isdir(project_root):
        raise NotADirectoryError(f'Project root {project_root} is not a directory')

    if project_root.endswith('Source'):
        project_root:str = utils.path.abspath(utils.path.join(project_root, '..'))

    src:str = utils.path.join(project_root, 'Source')

    for path in glob.iglob(f'{src}/**/Public', recursive=True):

        path:str = path.replace('\\', '/')

        frags:List[str] = path.split('/')
        name:str = frags[-2]
        module:str = utils.path.abspath(utils.path.join(path, '..'))

        cat:List[str] = extract_category(frags, 'Source', name)

        if not cat:
            cat = [name]

        yield Module(name, cat, module, [
            utils.path.join(module, 'Public'),
            utils.path.join(module, 'Private')
        ])


def find_plugins(project_root):
    src = utils.path.join(project_root, 'Plugins')

    for path in glob.iglob(f'{src}/**/Source', recursive=True):
        frags:List[str] = path.replace('\\', '/').split('/')
        path:str = path.replace('\\', '/')
        name:str = frags[-2]

        modules: List[Module] = find_modules(path)

        yield PluginModel(name=name, path=path, modules=modules)


def test_plugins(plugins_to_skip: List[str] = None):
    namespaces = set()
    tag_files: List[str] = []

    for i in find_plugins('E:/_00_blackdog/Docs/TestDocProject'):
        if plugins_to_skip and i.name in plugins_to_skip:
            print('skipping ', i.name)
            continue

        for module in find_modules(i.path):
            module.cat = [i.name]
            print('         module  : ', module.name, ' at path ', module.path, ' in plugin ', i.name)
            print('         cat     : ', module.cat)
            print('         tag_file: ', module.tagfile)
            print('         output  : ', module.output)

            namespaces.add('/'.join(module.cat))
            module.generate_documentation(gen_doxygen=True, other_tag_files=tag_files)

            tag_files.append(module.tagfile)


if __name__ == '__main__':
    test_plugins(plugins_to_skip=['KdsLogging', 'KdsMacroLib', 'RiderLink'])
