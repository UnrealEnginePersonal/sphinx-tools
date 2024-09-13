import glob
import os
from typing import List

from sphinx_tools.doxygen.module import Module


def extract_category(frags, start_tag, end_tag):
    cat = []
    cat_started = False

    for frag in frags:

        if frag == start_tag:
            cat_started = True
            continue

        if frag == end_tag:
            break

        if cat_started:
            cat.append(frag)

    return cat


def find_modules(project_root):
    src = os.path.join(project_root, 'Source')

    for path in glob.iglob(f'{src}/**/Public', recursive=True):
        frags = path.replace('\\', '/').split('/')

        name = frags[-2]
        module = os.path.abspath(os.path.join(path, '..'))

        cat = extract_category(frags, 'Source', name)
        if not cat:
            cat = [name]

        yield Module(name, cat, module, [
            os.path.join(module, 'Public'),
            os.path.join(module, 'Private')
        ])


class PluginModel:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path

    def get_modules(self) -> List[Module]:
        return list(find_modules('E:/_00_blackdog/Docs/TestDocProject/Plugins/' + self.name))


def find_modules_in_plugin(plugin: PluginModel) -> List[Module]:
    return plugin.get_modules()


def find_plugins(project_root):
    src = os.path.join(project_root, 'Plugins')

    for path in glob.iglob(f'{src}/**/Source', recursive=True):
        frags = path.replace('\\', '/').split('/')
        path = path.replace('\\', '/')
        name = frags[-2]
        yield PluginModel(name=name, path=path)


def test_modules():
    namespaces = set()
    for module in find_modules('E:/_00_blackdog/Docs/TestDocProject'):
        namespaces.add('/'.join(module.cat))


def test_plugins():
    namespaces = set()

    for i in find_plugins('E:/_00_blackdog/Docs/TestDocProject'):
        print(i.name, " at path ", i.path)

        if i.name == 'KdsLogging':
            print('skipping KdsLogging')
            continue

        if i.name == 'KdsMacroLib':
            print('skipping KdsMacroLib')
            continue

        for module in find_modules_in_plugin(i):
            print('         module: ', module.name, ' at path ', module.path, ' in plugin ', i.name)
            module.cat = [i.name]
            print('         cat: ', module.cat)
            namespaces.add('/'.join(module.cat))
            module.generate_documentation(gen_doxygen=True)

        # i.generate_documentation(gen_doxygen=True)


if __name__ == '__main__':
    test_plugins()
