import copy
import importlib.resources as resources
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import List, Union

from bs4 import BeautifulSoup
from typing_extensions import LiteralString

from sphinx_tools.version import get_version


def sanitize_filename(filename: str) -> str:
    # Remove or replace invalid characters like < > : " / \ | ? *
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def convert_union_to_str(union: Union[str, bytes, LiteralString]) -> str:
    un_decoded: Union[str, bytes] = union.decode() if isinstance(union, bytes) else union
    un_str: str = un_decoded if isinstance(un_decoded, str) else str(un_decoded)
    return un_str


@dataclass
class Conf:
    doxygen_out = None
    docs_src = None
    api_out = None
    projects = dict()


conf = Conf
# Set up configuration paths
conf_base_dir = 'E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/docs/'
conf.doxygen_out = conf_base_dir
conf.docs_src = conf_base_dir
conf.api_out = conf_base_dir


class Doxygen:
    values = {
        '@DOXYGEN_OUTPUT_DIR@': 'build',
        '@CMAKE_SOURCE_DIR@': '',
        '@PROJECT_NAME@': '',
        '@rev_branch@': 'archive',
        '@TAG_FILES@': '',
        '@GENERATE_HTML@': 'YES',
        '@PROJECT_TAG_FILE@': '',
        '@SOURCES@': '',
        '@IMAGE_PATH@': '',
    }

    def generate_config(self) -> str:
        """
        Generate a temp Doxygen configuration file from the template

        :return: The path to the generated file
        """
        # Use importlib.resources to access the Doxyfile.in template
        with resources.open_text(__package__, 'Doxyfile.in') as file:
            filedata = file.read()

        for key, value in self.values.items():
            if value is not None:
                filedata = filedata.replace(key, value)

        # create an temp file
        file_path = tempfile.NamedTemporaryFile(delete=False).name

        with open(file_path, 'w') as file:
            file.write(filedata)
            file_path = file.name
            file.close()

        return file_path

    def run(self):
        temp_file_path = self.generate_config()

        subprocess.call(f'doxygen {temp_file_path}', shell=True)
        os.remove(temp_file_path)


@dataclass
class Module:
    name: str
    cat: List[str]
    path: str
    sources: List[str]
    files: List[str] = field(default_factory=list)

    @property
    def output(self) -> str:
        out_dir: Union[str, bytes] = os.path.join(conf.doxygen_out, *self.cat, self.name)
        return out_dir

    @property
    def tagfile(self):
        return os.path.join(self.output, '_'.join(self.cat + [self.name]) + '.tag')

    def doxygen(self, tag=True):
        doxy = Doxygen()

        doxy.values['@DOXYGEN_OUTPUT_DIR@'] = self.output
        doxy.values['@CMAKE_SOURCE_DIR@'] = self.path
        doxy.values['@PROJECT_NAME@'] = self.name
        doxy.values['@rev_branch@'] = get_version()
        doxy.values['@TAG_FILES@'] = ''
        doxy.values['@GENERATE_HTML@'] = 'NO' if tag else 'YES'
        doxy.values['@PROJECT_TAG_FILE@'] = self.tagfile if tag else ''
        doxy.values['@SOURCES@'] = ' '.join(self.sources)
        doxy.values['@IMAGE_PATH@'] = os.path.join(conf.docs_src, '_static')

        return doxy

    def generate_documentation(self, gen_doxygen=False):
        print('=' * 40)
        print(f' Generating {"/".join(self.cat)} {self.name}')
        print('-' * 40)

        if gen_doxygen:
            dox = self.doxygen()
            if not os.path.exists(self.output):
                print(f'Creating API output for {self.name}')
                # create the output directory
                os.makedirs(self.output, exist_ok=True)
            dox.run()

        GeneratorFilePerClass(self).generate_api()
        print('-' * 40)

    @property
    def index_dir(self) -> str:
        path: Union[str, bytes] = os.path.join(conf.api_out, *self.cat)
        return path

    @property
    def index(self):
        return os.path.join(self.index_dir, self.name + '.rst')


KIND_TO_DIRECTIVE = {
    'class': 'doxygenclass',
    'struct': 'doxygenstruct',
    'define': 'doxygendefine',
    'enum': 'doxygendenum',
    'function': 'doxygenfunction',
    'interface': 'doxygeninterface',
    'typedef': 'doxygentypedef',
    'union': 'doxygenunion',
    'variable': 'doxygenvariable'
}

DOXYGEN_CLASS = """
{name}
{border}

.. {directive}:: {name}
   :project: {project}
   :protected-members:
   :private-members:
   :undoc-members:
"""

DOXYGEN_TOCTREE = """
{name}
{border}

.. toctree::
   :maxdepth: 1

{files}
"""

DOXYGEN_TOCTREE_GLOB = """
{cat}
{border}

.. toctree::
   :maxdepth: 1
   :glob:

   {cat}/*

"""


class GeneratorFilePerClass:
    def __init__(self, module: Module) -> None:
        self.mod = module

    def generate_api(self):
        print(f'Generating API rst from xml for {self.mod.name}')

        xml_dir = os.path.join(self.mod.output, 'xml')
        xml_index = os.path.join(xml_dir, 'index.xml')

        try:
            with open(xml_index, 'r') as f:
                index = BeautifulSoup(f, "xml")
        except FileNotFoundError:
            print(f"Missing XML file passing {xml_index}")
            return

        base_union: Union[LiteralString, str, bytes] = os.path.join(
            conf.api_out,
            *self.mod.cat,
            self.mod.name,
        )

        base_dir: str = convert_union_to_str(base_union)
        os.makedirs(base_dir, exist_ok=True)

        for comp in index.find_all("compound"):
            kind = comp.get('kind')

            if kind in ('file', 'dir'):
                continue

            name_tag = comp.find("name")
            name = name_tag.contents[0]

            file: str = os.path.join(base_dir, name + '.rst')
            print('file -----------------')
            print(file)

            self.mod.files.append(file)

            try:
                with open(file, 'w') as out:
                    directive = KIND_TO_DIRECTIVE.get(kind, 'doxygenclass')
                    out.write(DOXYGEN_CLASS.format(
                        name=name,
                        border='=' * len(name),
                        project=self.mod.name,
                        directive=directive,
                    ))
            except Exception as e:
                print(f'Error writing file {file}: {e}')

        path: str = convert_union_to_str(os.path.join(conf.api_out, *self.mod.cat))
        full_path: str = path + '\\'
        print('full_path -----------------')
        print(full_path)

        # get all the files map(lambda s: '   ' + s.replace('.rst', '').replace(path + '/', ''), self.mod.files))
        # remove .rst and path from the file name
        files = '\n'.join(map(lambda s: '   ' + s.replace('.rst', '').replace(full_path, ''), self.mod.files))

        # replace \ with / in the path
        files = files.replace('\\', '/')

        mod_index: str = self.mod.index
        print('mod_index -----------------')
        print(mod_index)

        with open(self.mod.index, 'w') as index:
            index.write(DOXYGEN_TOCTREE.format(
                name=self.mod.name,
                border='=' * len(self.mod.name),
                files=files,
            ))

        cats = copy.deepcopy(self.mod.cat)
        while cats:
            cat = cats.pop()
            toc_tree_file = os.path.join(conf.api_out, *cats, cat + '.rst')
            toc_tree_file_str = convert_union_to_str(toc_tree_file)
            print('toc_tree_file_str -----------------')
            print(toc_tree_file_str)

            with open(toc_tree_file_str, 'w') as f:
                f.write(DOXYGEN_TOCTREE_GLOB.format(cat=cat, border='=' * len(cat)))
