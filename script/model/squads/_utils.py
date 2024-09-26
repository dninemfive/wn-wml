from dataclasses import dataclass
from typing import Iterable, Literal, Self
from ndf_parse.model import List, ListRow, MemberRow, Object, Template

from managers.guid import GuidManager
from metadata.unit import UnitMetadata
from utils.collections import flatten, unique, with_indices
from utils.ndf import ensure

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

@dataclass
class Weapon(object):
    ammo_path: str
    effect_tag: str
    model_path: str
    weapon_type: Literal["'bazooka'", "'grenade'", "'mmg'", "'smg'"] | None = None

COUNTRY_CODE_TO_COUNTRY_SOUND_CODE = {
    'DDR': 'GER',
    'RFA': 'GER',
    'SOV': 'SOVIET',
    'UK': 'UK',
    'US': 'US'
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

def all_weapon_sub_depiction(metadata: UnitMetadata) -> str:
    return ensure.prefix(metadata.name, 'AllWeaponSubDepiction_')

def all_weapon_sub_depiction_backpack(metadata: UnitMetadata) -> str:
    return ensure.prefix(metadata.name, 'AllWeaponSubDepictionBackpack_')

def selector(unique_count: int, surrogates: int) -> str:
    return f'InfantrySelectorTactic_{str(unique_count).rjust(2, '0')}_{str(surrogates).rjust(2, '0')}'

def tactic_depiction_alternatives(metadata: UnitMetadata) -> str:
    return f'TacticDepiction_{metadata.name}_Alternatives'

class Squad(object):
    def __init__(self: Self, guids: GuidManager, country: str, *loadout: Weapon | list[Weapon] | tuple[int, list[Weapon]]):
        self.guids = guids
        self.country = country
        self.loadout: list[list[Weapon]] = []
        for item in loadout:
            if isinstance(item, Weapon):
                item = [item]
            if isinstance(item, list):
                item = (1, item)
            ct, weapons = item
            for i in range(ct):
                self.loadout.append(weapons)

    @property
    def total_soldiers(self: Self) -> int:
        return len(self.loadout)
    
    def gfx(self: Self) -> Object:
        return ensure._object('TemplateInfantryDepictionSquad',
                              SoundOperator=f'$/GFX/Sound/DepictionOperator_MovementSound_SM_Infanterie_{COUNTRY_CODE_TO_COUNTRY_SOUND_CODE[self.country]}')

    @property
    def unique_weapons_with_indices(self: Self) -> list[tuple[int, Weapon]]:
        return [with_indices([x for x in unique(flatten(self.loadout))], 1)]
    
    def all_weapon_alternatives(self: Self) -> List:
        result = List()
        unique_weapons = self.unique_weapons_with_indices
        for index, item in unique_weapons:
            result.add(ListRow(ensure._object(SelectorId=[mesh_alternative(index)],
                                              MeshDescriptor=item.model_path)))
        result.add(ListRow(ensure._object(SelectorId="'none'", ReferenceMeshForSkeleton=unique_weapons[-1][1].model_path)))
        return result
    
    def all_weapon_sub_depiction(self: Self, metadata: UnitMetadata):
        operators = List()
        for index, item in self.unique_weapons_with_indices:
            item: Weapon
            operators.add(ensure.listrow(ensure._object(
                'DepictionOperator_WeaponInstantFireInfantry',
                FireEffectTag=[item.effect_tag],
                WeaponShootDataPropertyName=f'"WeaponShootData_0_{index}"'
            )))
        return ensure._template('TemplateAllSubWeaponDepiction',
                                Alternatives=all_weapon_sub_depiction(metadata),
                                Operators=operators)
    
    def all_weapon_sub_depiction_backpack(self: Self, metadata: UnitMetadata) -> Template:
        return ensure._template('TemplateAllSubBackpackWeaponDepiction',
                                Alternatives=all_weapon_sub_depiction(metadata))
    
    # TacticDepiction_<unit>_Alternatives: just copy from wherever you're getting the models

    def conditional_tags(self: Self) -> List:
        result = List()
        for index, weapon in self.unique_weapons_with_indices:
            if weapon.weapon_type is not None:
                result.add(ensure.memberrow(weapon.weapon_type, mesh_alternative(index)))
        return result

    def tactic_depiction_soldier(self: Self, metadata: UnitMetadata, unique_count: int = 0, surrogates: int = 5) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryTactic',
                                Selector=selector(unique_count, surrogates),
                                Alternatives=tactic_depiction_alternatives(metadata),
                                SubDepictions=[all_weapon_sub_depiction(metadata), all_weapon_sub_depiction_backpack(metadata)],
                                Operators=ensure._object('DepictionOperator_SkeletalAnimation2_Default', ConditionalTags=self.conditional_tags()))
    
    def tactic_depiction_ghost(self: Self, metadata: UnitMetadata, unique_count: int = 0, surrogates: int = 5) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryGhost',
                                Selector=selector(unique_count, surrogates),
                                Alternatives=tactic_depiction_alternatives(metadata))