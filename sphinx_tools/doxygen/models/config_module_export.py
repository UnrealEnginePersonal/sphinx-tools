from dataclasses import dataclass

base_dir = 'E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools'
base_doxygen_dir = base_dir + '/generated/doxygen'
base_api_dir = base_dir + '/docs/api'

@dataclass
class ConfigModuleExport:
    doxygen_out: str = base_doxygen_dir
    module_api_out: str = base_api_dir
