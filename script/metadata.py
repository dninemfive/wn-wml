from dataclasses import dataclass
    
@dataclass
class ModMetadata(object):
    author: str
    name: str
    base_path: str
    version: str

    @property
    def source_path(self):
        return f'{self.base_path}{self.name} (input)'
    
    @property
    def output_path(self):
        return f'{self.base_path}{self.name}'

@dataclass
class DivisionMetadata(object):
    dev_short_name: str
    short_name: str
    country: str
    id: int
    
    def base_name(self, unit_name: str) -> str:
        return f'Unit_{self.dev_short_name}_{unit_name}_{self.country}'