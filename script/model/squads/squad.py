from typing import Self

from constants import ndf_paths
from managers.guid import GuidManager
from metadata.unit import UnitMetadata
from model.squads._utils import (COUNTRY_CODE_TO_COUNTRY_SOUND_CODE,
                                 mesh_alternative)
from model.squads.template_infantry_selector_tactic import \
    TemplateInfantrySelectorTactic
from model.squads.weapon import Weapon
from ndf_parse.model import (List, ListRow, Map, MapRow, MemberRow, Object,
                             Template)
from utils.collections import flatten, unique, with_indices
from utils.ndf import ensure
from utils.ndf.decorators import ndf_path


class Squad(object):
    def __init__(self: Self,
                 guids: GuidManager,
                 metadata: UnitMetadata,
                 country: str,
                 infantry_selector_tactic: TemplateInfantrySelectorTactic,
                 tactic_depiction: str | List,
                 *loadout: Weapon | list[Weapon] | tuple[int, list[Weapon]]):
        self.guids = guids
        self.metadata = metadata
        self.country = country
        self.infantry_selector_tactic = infantry_selector_tactic
        self.tactic_depiction = tactic_depiction
        self.loadout: list[list[Weapon]] = []
        for item in loadout:
            if isinstance(item, Weapon):
                item = [item]
            if isinstance(item, list):
                item = (1, item)
            ct, weapons = item
            for _ in range(ct):
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
    
    def all_weapon_sub_depiction(self: Self):
        operators = List()
        for index, item in self.unique_weapons_with_indices:
            item: Weapon
            operators.add(ensure.listrow(ensure._object(
                'DepictionOperator_WeaponInstantFireInfantry',
                FireEffectTag=[item.effect_tag],
                WeaponShootDataPropertyName=f'"WeaponShootData_0_{index}"'
            )))
        return ensure._template('TemplateAllSubWeaponDepiction',
                                Alternatives=self.all_weapon_sub_depiction_key,
                                Operators=operators)
    
    def all_weapon_sub_depiction_backpack(self: Self) -> Template:
        return ensure._template('TemplateAllSubBackpackWeaponDepiction',
                                Alternatives=self.all_weapon_sub_depiction_key)
    
    # TacticDepiction_<unit>_Alternatives: just copy from wherever you're getting the models

    def conditional_tags(self: Self) -> List:
        result = List()
        for index, weapon in self.unique_weapons_with_indices:
            if weapon.weapon_type is not None:
                result.add(ensure.memberrow(weapon.weapon_type, mesh_alternative(index)))
        return result

    def tactic_depiction_soldier(self: Self) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryTactic',
                                Selector=self.infantry_selector_tactic.name,
                                Alternatives=self.tactic_depiction_alternatives_key,
                                SubDepictions=[self.all_weapon_sub_depiction_key, self.all_weapon_sub_depiction_backpack_key],
                                Operators=ensure._object('DepictionOperator_SkeletalAnimation2_Default', ConditionalTags=self.conditional_tags()))
    
    def tactic_depiction_ghost(self: Self) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryGhost',
                                Selector=self.infantry_selector_tactic.name,
                                Alternatives=self.tactic_depiction_alternatives_key)
    @property
    def all_weapon_alternatives_key(self: Self) -> str:
        return ensure.prefix(self.metadata.name, 'AllWeaponAlternatives_')

    @property
    def all_weapon_sub_depiction_key(self: Self) -> str:
        return ensure.prefix(self.metadata.name, 'AllWeaponSubDepiction_')

    @property
    def all_weapon_sub_depiction_backpack_key(self: Self) -> str:
        return ensure.prefix(self.metadata.name, 'AllWeaponSubDepictionBackpack_')

    @property
    def tactic_depiction_alternatives_key(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Alternatives'

    @property
    def tactic_depiction_soldier_key(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Soldier'
    
    @property
    def tactic_depiction_ghost_key(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Ghost'

    @ndf_path(ndf_paths.GENERATED_DEPICTION_INFANTRY)
    def edit_generated_depiction_infantry(self: Self, ndf: List) -> None:
        ndf.add(ListRow(self.gfx(), namespace=f'Gfx_{self.metadata.name}'))
        ndf.add(ListRow(self.all_weapon_alternatives(), namespace=self.all_weapon_alternatives_key))
        ndf.add(ListRow(self.all_weapon_sub_depiction(), namespace=self.all_weapon_sub_depiction_key))
        ndf.add(ListRow(self.all_weapon_sub_depiction_backpack(), namespace=self.all_weapon_sub_depiction_backpack_key))
        if isinstance(self.tactic_depiction, str):
            self.tactic_depiction = ndf.by_name(self.tactic_depiction).value
        ndf.add(ListRow(self.tactic_depiction.copy(), namespace=self.tactic_depiction_alternatives_key))
        ndf.add(ListRow(self.tactic_depiction_soldier(), self.tactic_depiction_soldier_key))
        ndf.add(ListRow(self.tactic_depiction_ghost(), self.tactic_depiction_ghost_key))
        ndf.by_name('InfantryMimetic').value.add(MapRow(key=self.metadata.class_name_for_debug, value=self.tactic_depiction_soldier_key))
        ndf.by_name('InfantryMimeticGhost').value.add(MapRow(key=self.metadata.class_name_for_debug, value=self.tactic_depiction_ghost_key))
        ndf.by_name('TransportedInfantryAlternativesCount').value.add(ensure.maprow(self.metadata.class_name_for_debug,
                                                                                    self.infantry_selector_tactic.tuple))