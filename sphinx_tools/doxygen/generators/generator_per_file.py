from bs4 import BeautifulSoup

DOXYGEN_CLASS = """
{type} {class_name}
{border}

{type} Documentation
-------------------

.. {directive}:: {class_name}
    :project: {project}
    :members:
    :protected-members:
    :private-members:
    :undoc-members:
"""

DOXYGEN_TOCTREE = """
{name}
{border}

.. toctree::
   :caption: Classes
   :maxdepth: 1

{class_files}
"""

DOXYGEN_TOCTREE_GLOB = """
{cat}
{border}

.. toctree::
   :maxdepth: 2
   :glob:

   {cat}/*

"""

from sphinx_tools.doxygen.models.module import Module
from sphinx_tools.doxygen.utils import path as path_util


class GeneratorFilePerClass:
    def __init__(self, module: Module) -> None:
        self.mod = module
        path_util.recreate_dir(self.mod.base_module_api_dir)

    def generate_api(self):
        with open(self.mod.doxygen_xml_index_path, 'r') as f:
            index_file_data: BeautifulSoup = BeautifulSoup(f, "xml")

        index_compound_entries = index_file_data.find_all("compound")
        for index_compound_entry in index_compound_entries:
            kind: str = index_compound_entry.get('kind')

            if kind in ('file', 'dir'):
                continue

            name_tag = index_compound_entry.find("name")
            name = name_tag.contents[0]
            print(f'Processing {kind} {name}')

            if kind == 'class':
                self.document_class(name)

        files = '\n'.join(map(lambda s: '   ' + s.replace('.rst', '').replace(self.mod.parent_plugin_dir + '/', ''),
                              self.mod.succesfull_generated_api_files))
        files = files.replace('\\', '/')

        with open(self.mod.index_rst, 'w') as index_file_data:
            index_file_data.write(DOXYGEN_TOCTREE.format(
                name=self.mod.name,
                border='=' * len(self.mod.name),
                class_files=files
            ))

    def document_class(self, name) -> None:
        print(f'Documenting class {name}')

        type_str: str = 'Class'
        class_rst_file_path: str = path_util.join(self.mod.base_module_api_dir, f"class__{name}.rst")

        header_underline: str = '=' * len(f"{type_str} {name}")
        directive = 'doxygenclass'

        formatted_str: str = DOXYGEN_CLASS.format(
            border=header_underline,
            project=self.mod.name,
            directive=directive,
            class_name=name,
            type=type_str
        )

        try:
            with open(class_rst_file_path, 'w') as out:
                out.write(formatted_str)
                self.mod.succesfull_generated_api_files.append(class_rst_file_path)
        except Exception as e:
            print(f'Error writing file {class_rst_file_path}: {e}')
