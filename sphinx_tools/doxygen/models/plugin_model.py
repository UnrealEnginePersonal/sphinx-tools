from dataclasses import dataclass
from typing import List

from .module import Module

@dataclass
class PluginModel:
    def __init__(self, name: str, path: str, modules: List[Module]) -> None:
        self.name = name
        self.path = path
        self.modules = modules
