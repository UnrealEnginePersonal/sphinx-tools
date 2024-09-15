from typing import List

from sphinx_tools.doxygen.utils import plugins as plugin_utils


class PluginModel:
    def __init__(self, name: str, source_path: str) -> None:
        self.name: str = name
        self.source_path = source_path
        self.generated_modules = []
        self.generated_tag_files = []

    def generate_api_docs(self, external_tag_files: List[str] = None, second_pass: bool = False) -> None:
        if external_tag_files:
            self.generated_tag_files = external_tag_files

        for module in plugin_utils.find_modules(self.source_path):
            print('--'.center(150, '-'))
            print('         module  : ', module.name, ' at path ', module.path, ' in plugin ', self.name)
            print('         cat     : ', module.cat)
            print('         output  : ', module.doxygen_out_path)
            print('--'.center(150, '-'))

            module = module.generate_documentation(gen_doxygen=True, other_tag_files=self.generated_tag_files, second_pass=second_pass)

            if not second_pass:
                self.generated_tag_files.append(module.tagfile_path)
                self.generated_modules.append(module)
