import os
import subprocess
from dataclasses import dataclass, field
import tempfile
import pkg_resources
import copy

from sphinx_tools.version import get_version

from bs4 import BeautifulSoup


@dataclass
class Conf:
    doxygen_out = None
    docs_src = None
    doxyfile_folder = None
    api_out = None
    projects = dict()


conf = Conf


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

    def generate_config(self):
        template = pkg_resources.resource_filename(__name__, 'Doxyfile.in')

        with open(template, 'r') as file:
            filedata = file.read()

        for key, value in self.values.items():

            if value is not None:
                filedata = filedata.replace(key, value)

        file = tempfile.NamedTemporaryFile()
        file.write(filedata.encode('utf-8'))
        return file

    def run(self):
        tmpfile = self.generate_config()
        tmpfile.flush()
        subprocess.call(f'doxygen {tmpfile.name}', shell=True)
        tmpfile.close()

@dataclass
class Module:
    name: str
    cat: list[str]
    path: str
    sources: list[str]
    files: list[str] = field(default_factory=list)

    @property
    def output(self):
        return os.path.join(conf.doxygen_out, *self.cat, self.name)

    @property
    def tagfile(self):
        return os.path.join(self.output, '_'.join(self.cat + [self.name]) + '.tag')

    @property
    def doxygen_config(self):
        return f'{conf.doxyfile_folder}/Doxyfile_{self.name}'

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

    def generate_documentation(self):
        print('=' * 40)
        print(f' Generating {"/".join(self.cat)} {self.name}')
        print('-' * 40)

        dox = self.doxygen()
        dox.run()

        GeneratorFilePerClass(self).generate_api()
        print('-' * 40)

    @property
    def index_dir(self):
        return os.path.join(conf.api_out, *self.cat)

    @property
    def index(self):
        return os.path.join(self.index_dir, self.name + '.rst')


KIND_TO_DIRECTIVE = {
    'class': 'doxygenclass',
    'struct': 'doxygenstruct',
    'define': 'doxygendefine',
    'enum':  'doxygendenum',
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

DOXYGEN_TOCTREE_GLOB =  """
{cat}
{border}

.. toctree::
   :maxdepth: 1
   :glob:

   {cat}/*

"""


class GeneratorFilePerClass:
    def __init__(self, module) -> None:
        self.mod = module

    def generate_api(self):
        xml_dir = os.path.join(self.mod.output, 'xml')
        xml_index = os.path.join(xml_dir, 'index.xml')

        try:
            with open(xml_index, 'r') as f:
                index = BeautifulSoup(f, "xml")
        except FileNotFoundError:
            print(f"Missing XML file passing {xml_index}")
            return

        base_dir = os.path.join(
            conf.api_out,
            *self.mod.cat,
            self.mod.name,
        )
        os.makedirs(base_dir, exist_ok=True)

        for comp in index.find_all("compound"):
            kind = comp.get('kind')

            if kind in ('file', 'dir'):
                continue

            name_tag = comp.find("name")
            name = name_tag.contents[0]
            file = os.path.join(base_dir, name + '.rst')

            self.mod.files.append(file)
            with open(file, 'w') as out:
                directive = KIND_TO_DIRECTIVE.get(kind, 'doxygenclass')
                out.write(DOXYGEN_CLASS.format(
                    name=name,
                    border='=' * len(name),
                    project=self.mod.name,
                    directive=directive,
                ))

        path = os.path.join(conf.api_out, *self.mod.cat)
        files = '\n'.join(map(lambda s: '   ' + s.replace('.rst', '').replace(path + '/', ''), self.mod.files))

        with open(self.mod.index, 'w') as index:
            index.write(DOXYGEN_TOCTREE.format(
                name=self.mod.name,
                border='=' * len(self.mod.name),
                files=files,
            ))


        cats = copy.deepcopy(self.mod.cat)
        while cats:
            cat = cats.pop()

            with open(os.path.join(conf.api_out, *cats, cat + '.rst'), 'w') as f:
                f.write(DOXYGEN_TOCTREE_GLOB.format(cat=cat, border='=' * len(cat)))
