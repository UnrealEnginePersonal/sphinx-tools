from dataclasses import dataclass

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


@dataclass
class CompoundDirective:
    def __init__(self, name: str, kind: str, rst_file: str):
        self.name = name
        self.kind = kind
        self.rst_file = rst_file
