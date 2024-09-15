import os.path as ospath
import sys

sys.path.append(ospath.abspath(ospath.join(ospath.dirname(__file__), '..')))

import glob
from typing import List
from sphinx_tools.doxygen.models.plugin import PluginModel
from sphinx_tools.doxygen.utils import path as utils


def find_plugins(project_root) -> List[PluginModel]:
    src = utils.join(project_root, 'Plugins')

    for path in glob.iglob(f'{src}/**/Source', recursive=True):
        frags: List[str] = path.replace('\\', '/').split('/')
        path: str = path.replace('\\', '/')
        name: str = frags[-2]

        yield PluginModel(name=name, source_path=path)


def test_plugins(plugins_to_skip: List[str] = None):
    if plugins_to_skip is None:
        plugins_to_skip = []

    _base_dir = 'E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools'

    _doxygen_dir = utils.join(_base_dir, 'generated')
    _api_dir = utils.join(_base_dir, 'docs', 'api')
    _api_dir = utils.abspath(_api_dir)
    _build_dir = utils.join(_base_dir, 'docs', '_build')

    utils.remove_dir(_doxygen_dir)
    utils.remove_dir(_api_dir)
    utils.remove_dir(_build_dir)

    generated_tag_files = []
    generated_plugins: List[PluginModel] = []

    for plugin in find_plugins('E:/_00_blackdog/Docs/TestDocProject'):
        print('=='.center(200, '='))

        if plugins_to_skip and plugin.name in plugins_to_skip:
            print('skipping ', plugin.name)
            continue

        print('plugin: ', plugin.name, ' at path ', plugin.source_path)

        plugin.generate_api_docs(external_tag_files=generated_tag_files)
        generated_tag_files = plugin.generated_tag_files
        generated_plugins.append(plugin)

        print('=='.center(250, '='))

    print('generated_plugins: ', generated_plugins)


    print('=='.center(1000, '='))
    print('=='.center(1000, '='))
    print('=='.center(1000, '='))
    print('SECOND PASS'.center(1000, '='))
    print('=='.center(1000, '='))
    print('=='.center(1000, '='))
    #swap the order of the plugins
    generated_plugins.reverse()

    for plugin in generated_plugins:
        print('=='.center(250, '='))
        print('plugin: ', plugin.name, ' at path ', plugin.source_path)
        plugin.generate_api_docs(external_tag_files=generated_tag_files, second_pass=True)
        print('=='.center(250, '='))



if __name__ == '__main__':
    test_plugins(plugins_to_skip=[])
