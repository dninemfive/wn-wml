from typing import Iterable, Self
from ndf_parse.model import List, ListRow, MemberRow, Object, Template

from managers.guid import GuidManager
from metadata.unit import UnitMetadata
from utils.collections import flatten, unique
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

class Weapon(object):
    def __init__(self: Self, ammo_path: str, effect_tag: str, model_path: str):
        self.ammo_path = ammo_path
        self.effect_tag = effect_tag
        self.model_path = model_path

COUNTRY_CODE_TO_COUNTRY_SOUND_CODE = {
    'DDR': 'GER',
    'RFA': 'GER',
    'SOV': 'SOVIET',
    'UK': 'UK',
    'US': 'US'
}

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
    def unique_weapons(self: Self) -> list[Weapon]:
        return [x for x in unique(flatten(self.loadout))]
    
    def all_weapon_alternatives(self: Self) -> List:
        index: int = 1
        result = List()
        unique_weapons = self.unique_weapons
        for item in unique_weapons:
            result.add(ListRow(ensure._object(SelectorId=[f"'MeshAlternative_{index}'"],
                                              MeshDescriptor=item.model_path)))
        result.add(ListRow(ensure._object(SelectorId="'none'", ReferenceMeshForSkeleton=unique_weapons[-1].model_path)))
        return result
    
    def all_weapon_sub_depiction(self: Self, metadata: UnitMetadata):
        result = Template('TemplateAllSubWeaponDepiction')
        result.add(ensure.memberrow('Alternatives', ensure.prefix(metadata.name, 'AllWeaponSubDepiction_')))
        index: int = 1
        operators = List()
        for item in self.unique_weapons:
            operators.add(ensure.listrow(ensure._object(
                'DepictionOperator_WeaponInstantFireInfantry',
                FireEffectTag=[item.effect_tag],
                WeaponShootDataPropertyName=f'WeaponShootData_0_{index}'
            )))
            index += 1
        result.add(ensure.memberrow('Operators', operators))
        return result
    
    def all_weapon_sub_depiction_backpack(self: Self, metadata: UnitMetadata) -> Template:
        result = Template()
        result.add(MemberRow('', ensure.prefix(metadata.name, 'AllWeaponSubDepiction_')))
        return result
