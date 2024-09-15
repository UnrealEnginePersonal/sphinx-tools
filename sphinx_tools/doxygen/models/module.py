import importlib.resources as resources
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import List, Dict

from sphinx_tools.version import get_version


class Doxygen:
    values: Dict[str, str] = {
        '@DOXYGEN_OUTPUT_DIR@': 'build',
        '@CMAKE_SOURCE_DIR@': '',
        '@PROJECT_NAME@': '',
        '@rev_branch@': 'archive',
        '@TAG_FILES@': '',
        '@GENERATE_HTML@': 'YES',
        '@PROJECT_TAG_FILE@': '',
        '@SOURCES@': ''
    }

    def generate_config(self) -> str:
        """
        Generate a temp Doxygen configuration file from the template

        Returns:
            The path to the temp generated configuration file
        """
        # Use importlib.resources to access the Dotfile.in template
        with resources.open_text(__package__, 'Doxyfile.in') as file:
            filedata = file.read()

        for key, value in self.values.items():
            if value is not None:
                filedata = filedata.replace(key, value)

        file_path: str = tempfile.NamedTemporaryFile(delete=False).name

        with open(file_path, 'w') as file:
            file.write(filedata)
            file_path = file.name
            file.close()

        return file_path

    def run(self) -> None:
        """
        Run Doxygen with the generated configuration file

        Returns:
            None
        """
        temp_file_path = self.generate_config()
        subprocess.call(f'doxygen {temp_file_path}', shell=True)
        os.remove(temp_file_path)



from sphinx_tools.doxygen.utils import path as path_util

@dataclass
class Module:
    from sphinx_tools.doxygen.models.config_module_export import ConfigModuleExport

    name: str
    cat: List[str]
    path: str
    sources: List[str]

    succesfull_generated_api_files: List[str] = field(default_factory=list)
    export_config: ConfigModuleExport = field(default_factory=ConfigModuleExport)

    @property
    def doxygen_out_path(self) -> str:
        """
        Get the path to the Doxygen output directory for the module

        Returns:
            The path to the Doxygen output directory for the module
        """
        return path_util.join(self.export_config.doxygen_out, *self.cat, self.name)

    @property
    def tagfile_path(self) -> str:
        """
        Get the path to the tag file for the module

        Returns:
            The path to the tag file
        """
        return path_util.join(self.doxygen_out_path, '_'.join(self.cat + [self.name]) + '.tag')

    @property
    def doxygen_xml_path(self) -> str:
        """
        Get the path to the Doxygen XML output file

        Returns:
            The path to the Doxygen XML output file
        """
        return path_util.join(self.doxygen_out_path, 'xml')

    @property
    def doxygen_xml_index_path(self) -> str:
        """
        Get the path to the Doxygen XML index file

        Returns:
            The path to the Doxygen XML index file
        """
        return path_util.join(self.doxygen_xml_path, 'index.xml')

    @property
    def parent_plugin_dir(self) -> str:
        return path_util.join(self.export_config.module_api_out, *self.cat)

    @property
    def base_module_api_dir(self) -> str:
        return path_util.join(self.parent_plugin_dir, self.name)

    @property
    def index_rst(self) -> str:
        index_rst_name: str = self.name +'_index.rst'
        return path_util.join(self.parent_plugin_dir, index_rst_name)

    def generate_tagfile_str(self, files: List[str]) -> str:
        """
        Generate a string for the TAGFILES doxygen configuration option

        This will generate a string that includes all the tag files provided in the list, in the format required by
        the Doxygen configuration file.


        Args:
            files (List[str]): A list of tag files to include in the configuration

        Returns:
            A string for the TAGFILES configuration option, and empty string if no files are provided

        Example:
            >>> Module.generate_tagfile_str(['tagfile0', 'tagfile1', 'tagfile2', 'tagfile3'])
            TAGFILES  = "tagfile0" \n
            TAGFILES  += "tagfile1" \n
            TAGFILES  += "tagfile2" \n
            TAGFILES  += "tagfile3" \n
        """
        if not files:
            return "TAGFILES  = "

        if len(files) == 1:
            # check if the tagfile is the same as the project tagfile
            if files[0] == self.tagfile_path:
                return f"TAGFILES  ="
            else:
                return f"TAGFILES  = {files[0]}"

        if files[0] == self.tagfile_path:
            files = files[1:]

        result: str = "TAGFILES  = " + files[0] + "\n"
        for file in files[1:]:
            if file == self.tagfile_path:
                continue
            result += f"TAGFILES  += {file}\n"

        return result


    def generate_input_str(self, inputs: List[str]) -> str:
        """
        Generate a string for the INPUT doxygen configuration option

        This will generate a string that includes all the input directories provided in the list, in the format required
        by the Doxygen configuration file.


        Args:
            inputs (List[str]): A list of input directories to include in the configuration

        Returns:
            A string for the INPUT configuration option, and empty string if no directories are provided

        Example:
            >>> Module.generate_input_str(['dir0', 'dir1', 'dir2', 'dir3'])
            INPUT  = "dir0" \n
            INPUT  += "dir1" \n
            INPUT  += "dir2" \n
            INPUT  += "dir3" \n
        """
        result: str = "INPUT  = " + inputs[0] + "\n"

        for in_file in inputs[1:]:
            result += f"INPUT  += {in_file}\n"

        return result

    def doxygen(self, tag: bool = True, other_tag_files: List[str] = None) -> Doxygen:
        """"
        Generate a Doxygen config data object for the module.


        Args:
            tag: Whether to generate a tag file for the module
            other_tag_files: A list of other tag files to include in the configuration

        Returns:
            A Doxygen object for the module
        """

        doxy: Doxygen = Doxygen()
        doxy.values['@DOXYGEN_OUTPUT_DIR@'] = self.doxygen_out_path
        doxy.values['@CMAKE_SOURCE_DIR@'] = self.path
        doxy.values['@PROJECT_NAME@'] = self.name
        doxy.values['@rev_branch@'] = get_version()

        tag_files_conf: str = self.generate_tagfile_str(other_tag_files)
        doxy.values['@TAG_FILES@'] = tag_files_conf

        doxy.values['@GENERATE_HTML@'] = 'NO' if tag else 'YES'
        doxy.values['@PROJECT_TAG_FILE@'] = self.tagfile_path if tag else ''
        #doxy.values['@SOURCES@'] = ' '.join(self.sources)

        source_conf: str = self.generate_input_str(self.sources)
        doxy.values['@SOURCES@'] = source_conf

        return doxy

    def generate_documentation(self,
                               gen_doxygen=False, other_tag_files: List[str] = None, second_pass: bool = False)  -> 'Module':
        """
        Generate the documentation for the module

        This will generate the Doxygen documentation for the module if gen_doxygen is True, and generate the API documentation
        if this is the second pass of the documentation generation.

        Args:
            gen_doxygen: Whether to generate Doxygen documentation
            other_tag_files: A list of other tag files to include in the configuration
            second_pass: If this is the second pass of the documentation generation

        Returns:
             self: The current instance of the Module class
        """
        if gen_doxygen:
            path_util.recreate_dir(self.doxygen_out_path)
            dox: Doxygen = self.doxygen(other_tag_files=other_tag_files)
            dox.run()

        if second_pass:
            from sphinx_tools.doxygen.generators.generator_per_file import GeneratorFilePerClass
            GeneratorFilePerClass(self).generate_api()

        return self
