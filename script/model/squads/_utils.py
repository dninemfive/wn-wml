from dataclasses import dataclass
from typing import Iterable, Literal, Self

from managers.guid import GuidManager
from metadata.unit import UnitMetadata
from ndf_parse.model import (List, ListRow, Map, MapRow, MemberRow, Object,
                             Template)
from utils.collections import flatten, unique, with_indices
from utils.ndf import ensure

from script.constants import ndf_paths
from script.utils.ndf.decorators import ndf_path


def adjust_squad(squad: Object, *loadouts: tuple[int, list[str] | list[str]]) -> None:
    # for loadout in loadouts
    # add tuple[1] ct of soldiers (default 1 if ct not included) with the specified loadout
    # create custom gfx depiction based on this
    # create showroom unit
    raise NotImplemented
    # things which need to be changed:
    # ApparenceModel
    # new TemplateAllSubWeaponDepiction
    # WeaponManager -> new WeaponDescriptor
    # TBaseDamageModuleDescriptor.MaxPhysicalDamages = sum(k for k in loadouts)
    # TDangeroussnessModuleDescriptor proportional to weapons and size
    # GroupeCombat.Default.NbSoldatInGroupeCombat = ct
    # TacticalLabelModuleDescriptor
    # bounding box
    # showroom unit
    # add new gfx to InfantryMimetic

COUNTRY_CODE_TO_COUNTRY_SOUND_CODE = {
    'DDR':  'GER',
    'RFA':  'GER',
    'SOV':  'SOVIET',
    'UK' :  'UK',
    'US' :  'US',
    'POL':  'SOVIET'
}

VALID_WEAPON_TYPES = [
    None,
    "'bazooka'",
    "'grenade'",
    "'mmg'",
    "'smg'"
]

def mesh_alternative(index: int) -> str:
    return f"'MeshAlternative_{index}'"

def _0(n: int) -> str:
    return f'_{str(n).rjust(2, '0')}'