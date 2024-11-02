from dataclasses import dataclass
from typing import Literal, Self

from utils.ndf import ensure
from utils.localization import delocalize

@dataclass(frozen=True)
class NamePathPair(object):
    _path: str
    _prefix: str
    _base_name: str
    _suffix: str = ""

    @property
    def name(self: Self) -> str:
        return f'{self._prefix}{self._base_name}{self._suffix}'
    
    @property
    def path(self: Self) -> str:
        return f'{self._path}{self.name}'
    
_pos_t = Literal['Before', 'After']
_fix_t = Literal['Prefix', 'Suffix']
ShowroomPosition = tuple[_pos_t, _fix_t]

@dataclass(frozen=True)
class NamePathPairWithShowroomEquivalent(NamePathPair):
    _showroom: str = 'Showroom'
    _showroom_position: ShowroomPosition = ('Before', 'Suffix')
    
    @property
    def _showroom_name(self: Self) -> str:
        def sia(pos: _pos_t, fix: _fix_t) -> str:
            """ showroom if appropriate """
            return self._showroom if self._showroom_position == (pos, fix) else ''
        def fix(value: str,
                key: _fix_t) -> str:
            return f'{sia('Before', key)}{value}{sia('After', key)}'
        prefix = fix(self._prefix, 'Prefix')
        suffix = fix(self._suffix, 'Suffix')
        return f'{prefix}{self._base_name}{suffix}'

    @property
    def showroom(self: Self) -> NamePathPair:
        return NamePathPair(self._path, '', self._showroom_name)

@dataclass(frozen=True)
class UnitMetadata(object):
    name: str

    # unpaired properties    
    @property
    def button_texture_name(self: Self) -> str:
        return f'Texture_Button_Unit_{self.name}'
    
    @property
    def class_name_for_debug(self: Self) -> str:
        return f"'Unit_{self.name}'"
    
    @property
    def quoted_name(self: Self) -> str:
        return f"'{self.name}'"
    
    @property
    def tag(self: Self) -> str:
        return f'"UNITE_{self.name}"'
    
    # paired properties    
    @property
    def deck_pack_descriptor(self: Self) -> NamePathPair:
        return NamePathPair('~/', 'Descriptor_Deck_Pack_', self.name)
    
    @property
    def weapon_descriptor(self: Self) -> NamePathPair:
        return NamePathPair('$/GFX/Weapon/', 'WeaponDescriptor_', self.name)
    
    # paired properties with showroom equivalents    
    @property
    def descriptor(self: Self) -> NamePathPairWithShowroomEquivalent:
        return NamePathPairWithShowroomEquivalent(
            '$/GFX/Unit/',
            'Descriptor_',
            f'Unit_{self.name}',
            _showroom='ShowRoom',
            _showroom_position=('After', 'Prefix')
        )
    
    @property
    def gfx_autogen(self: Self) -> NamePathPairWithShowroomEquivalent:
        return NamePathPairWithShowroomEquivalent(
            '~/',
            'Gfx_',
            self.name,
            '_Autogen'
        )
    
    @property
    def missile_carriage(self: Self) -> NamePathPairWithShowroomEquivalent:
        return NamePathPairWithShowroomEquivalent(
            '',
            'MissileCarriage_',
            self.name,
            _showroom_position = ('After', 'Suffix')
        )
    
    @property
    def subgenerators(self: Self) -> NamePathPairWithShowroomEquivalent:
        return NamePathPairWithShowroomEquivalent(
            '',
            'SubGenerators_',
            self.name,
            _showroom_position=('After', 'Prefix')
        )
    
    # static methods
    @staticmethod
    def from_localized_name(prefix: str, localized_name: str, country: str) -> Self:
        return UnitMetadata(f"{prefix}_{delocalize(localized_name)}_{country}")
    
    @staticmethod
    def resolve(val: str | Self) -> Self:
        if isinstance(val, str):
            return UnitMetadata(ensure.no_prefix(val, 'Descriptor_Unit_'))
        if isinstance(val, UnitMetadata):
            return val
        raise TypeError(f'Cannot resolve an object of type {type(val).__name__} to UnitMetadata!')
    
    @staticmethod
    def try_resolve(val: str | Self | None, backup: str | Self) -> Self:
        if val is not None:
            return UnitMetadata.resolve(val)
        return UnitMetadata.resolve(backup)