from typing import Self

import constants.ndf_paths as ndf_paths
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from constants import ndf_paths
from creators.unit import UnitCreator
from managers.guid import GuidManager
from metadata.unit import UnitMetadata
from model.squads._squad_keys import _SquadKeys
from model.squads.infantry_weapon_set import InfantryWeaponSet
from model.squads.template_infantry_selector_tactic import \
    TemplateInfantrySelectorTactic
from ndf_parse.model import (List, ListRow, Map, MapRow, MemberRow, Object,
                             Template)
from utils.ndf import ensure
from utils.ndf.decorators import ndf_path
from utils.types.message import Message


def _mesh_alternative(index: int) -> str:
    return f"'MeshAlternative_{index}'"

class Squad(object):
    def __init__(self: Self,
                 guids: GuidManager,
                 creator: UnitCreator,
                 country: str,
                 weapon_set: InfantryWeaponSet,
                 copy_of: str | UnitMetadata | None = None):
        self.guids = guids
        self.metadata = creator.new
        self.country = country
        self.copy_of = UnitMetadata(copy_of if copy_of is not None else creator.src.name)
        self.weapon_set = weapon_set
        self._keys = _SquadKeys(self.metadata)
        self._cached_weapon_assignment: dict[int, list[int]] | None = None

    # properties

    @property
    def soldier_count(self: Self) -> int:
        return sum(weapon.count for weapon in self.weapon_set if not weapon.is_secondary)
    
    # internal methods

    def _gfx(self: Self) -> Object:
        return ensure._object('TemplateInfantryDepictionSquad',
                              SoundOperator=f'$/GFX/Sound/DepictionOperator_MovementSound_SM_Infanterie_{ensure.country_sound_code[self.country]}')    
    
    def _all_weapon_alternatives(self: Self) -> List:
        result = List()
        for weapon in self.weapon_set:
            result.add(ListRow(ensure._object(SelectorId=[_mesh_alternative(weapon.index)],
                                              MeshDescriptor=weapon.model_path)))
        result.add(ListRow(ensure._object(SelectorId="'none'", ReferenceMeshForSkeleton=self.weapon_set.last.model_path)))
        return result
    
    def _all_weapon_sub_depiction(self: Self):
        operators = List()
        for weapon in self.weapon_set:
            operators.add(ensure.listrow(ensure._object(
                'DepictionOperator_WeaponInstantFireInfantry',
                FireEffectTag=[weapon.effect_tag],
                WeaponShootDataPropertyName=f'"WeaponShootData_0_{weapon.index}"'
            )))
        return ensure._template('TemplateAllSubWeaponDepiction',
                                Alternatives=self._keys._all_weapon_sub_depiction,
                                Operators=operators)
    
    def _all_weapon_sub_depiction_backpack(self: Self) -> Template:
        return ensure._template('TemplateAllSubBackpackWeaponDepiction',
                                Alternatives=self._keys._all_weapon_sub_depiction)

    def _conditional_tags(self: Self) -> List:
        result = List()
        for weapon in self.weapon_set:
            if weapon.type is not None:
                result.add(ensure.memberrow(weapon.type, _mesh_alternative(weapon.index)))
        return result

    def _tactic_depiction_soldier(self: Self, selector_tactic: TemplateInfantrySelectorTactic) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryTactic',
                                Selector=selector_tactic.name,
                                Alternatives=self._keys._tactic_depiction_alternatives,
                                SubDepictions=[self._keys._all_weapon_sub_depiction, self._keys._all_weapon_sub_depiction_backpack],
                                Operators=ensure._object('DepictionOperator_SkeletalAnimation2_Default', ConditionalTags=self._conditional_tags()))
    
    def _tactic_depiction_ghost(self: Self, selector_tactic: TemplateInfantrySelectorTactic) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryGhost',
                                Selector=selector_tactic.name,
                                Alternatives=self._keys._tactic_depiction_alternatives)

    @ndf_path(ndf_paths.GENERATED_DEPICTION_INFANTRY)
    def edit_generated_depiction_infantry(self: Self, ndf: List) -> None:
        ndf.add(ListRow(self._gfx(), namespace=f'Gfx_{self.metadata.name}'))
        ndf.add(ListRow(self._all_weapon_alternatives(), namespace=self._keys._all_weapon_alternatives))
        ndf.add(ListRow(self._all_weapon_sub_depiction(), namespace=self._keys._all_weapon_sub_depiction))
        ndf.add(ListRow(self._all_weapon_sub_depiction_backpack(), namespace=self._keys._all_weapon_sub_depiction_backpack))
        tactic_depiction: Object = ndf.by_name(ensure.prefix_and_suffix(self.copy_of.name, 'TacticDepiction_', '_Alternatives')).value
        ndf.add(ListRow(tactic_depiction.copy(), namespace=self._keys._tactic_depiction_alternatives))
        selector_tactic: TemplateInfantrySelectorTactic\
            = TemplateInfantrySelectorTactic.from_tuple(ndf.by_name('TransportedInfantryAlternativesCount').value\
                                                           .by_key(self.copy_of.quoted_name).value)
        ndf.add(ListRow(self._tactic_depiction_soldier(selector_tactic), self._keys._tactic_depiction_soldier))
        ndf.add(ListRow(self._tactic_depiction_ghost(selector_tactic), self._keys._tactic_depiction_ghost))
        ndf.by_name('InfantryMimetic').value.add(MapRow(key=self._keys._unit, value=self._keys._tactic_depiction_soldier))
        ndf.by_name('InfantryMimeticGhost').value.add(MapRow(key=self._keys._unit, value=self._keys._tactic_depiction_ghost))
        ndf.by_name('TransportedInfantryAlternativesCount').value.add(ensure.maprow(self._keys._unit,
                                                                                    selector_tactic.tuple))
        
    def apply(self: Self, ndf: dict[str, List], msg: Message | None) -> None:
        self.edit_generated_depiction_infantry(ndf, msg)

    def _make_infantry_squad_module_descriptor(self: Self, guid_key: str) -> Object:
        return ensure._object('TInfantrySquadModuleDescriptor',
                              NbSoldatInGroupeCombat=self.soldier_count,
                              InfantryMimeticName=self._keys._unit,
                              WeaponUnitFXKey=self._keys._unit,
                              MimeticDescriptor=ensure._object('Descriptor_Unit_MimeticUnit', 
                                                               DescriptorId=self.guids.generate(guid_key),
                                                               MimeticName=self._keys._unit),
                              BoundingBoxSize=f'{self.soldier_count + 2} * Metre')

    def _edit_groupe_combat(self: Self, module: Object) -> None:
        edit.members(module,
                     Default=self._make_infantry_squad_module_descriptor(f'{self.metadata.descriptor_name}/ModulesDescriptors["GroupeCombat"]/Default/MimeticDescriptor'))

    def _create_infantry_squad_weapon_assignment(self: Self) -> Object:
        if self._cached_weapon_assignment is None:
            turrets: dict[int, list[int]] = {}
            soldier_index = 0
            secondaries = list(self.weapon_set.secondaries_in_order)
            secondary_count = sum(x.count for x in secondaries)
            for primary in self.weapon_set.primaries_in_reverse_order:
                remaining_soldiers = self.soldier_count - soldier_index - 1
                this_soldier_weapons = [primary.index]

                turrets[soldier_index] = [primary.index]
                # TODO: handle secondaries
                soldier_index += 1
            self._cached_weapon_assignment = turrets
        return ensure._object('TInfantrySquadWeaponAssignmentModuleDescriptor',
                               InitialSoldiersToTurretIndexMap=turrets)
        
    @ndf_path(ndf_paths.SHOWROOM_UNITS)
    def edit_showroom_units(self: Self, ndf: List):
        copy: Object = ndf.by_name(self.copy_of.showroom_descriptor_name).value.copy()
        edit.members(copy,
                     DescriptorId=self.guids.generate(self.copy_of.showroom_descriptor_name))
        module.replace_where(copy, self.metadata.weapon_descriptor_path, lambda x: x.value.startswith('$/GFX/Weapon/'))
        module.replace_module(copy,
                              self._make_infantry_squad_module_descriptor(module.path_by_type(self.copy_of.showroom_descriptor_name,
                                                                                             'TInfantrySquadModuleDescriptor',
                                                                                             'MimeticDescriptor',
                                                                                             'DescriptorId')),
                              'TInfantrySquadModuleDescriptor')
        module.replace_module(copy,
                              self._create_infantry_squad_weapon_assignment().copy(),
                              'TInfantrySquadWeaponAssignmentModuleDescriptor')
        
    @ndf_path(ndf_paths.WEAPON_DESCRIPTOR)
    def edit_weapon_descriptors(self: Self, ndf: List):
        ndf.add(ListRow(self.weapon_set.to_weapon_descriptor(), 'export', self.metadata.weapon_descriptor_name))
    
    def edit_unit(self: Self, unit: UnitCreator) -> None:
        unit.edit_module_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=self.soldier_count)        
        self._edit_groupe_combat(unit.get_module('GroupeCombat', by_name=True))
        unit.replace_module(self._create_infantry_squad_weapon_assignment(), 'TInfantrySquadWeaponAssignmentModuleDescriptor')
        unit.edit_module_members('TTacticalLabelModuleDescriptor', NbSoldiers=self.soldier_count)
        unit.edit_module_members('WeaponManager', by_name=True, Default=self.metadata.weapon_descriptor_path)
        unit.showroom_src = UnitMetadata(self.copy_of)