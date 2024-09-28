from typing import TYPE_CHECKING, Self

import constants.ndf_paths as ndf_paths
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from constants import ndf_paths
from creators.unit.basic import UnitCreator
from creators.unit.utils.infantry._squad_keys import _SquadKeys
from creators.unit.utils.infantry.weapon import InfantryWeapon
from creators.unit.utils.infantry.weapon_set import InfantryWeaponSet
from managers.guid import GuidManager
from metadata.new_unit import NewUnitMetadata
from metadata.unit import UnitMetadata
from ndf_parse.model import (List, ListRow, Map, MapRow, MemberRow, Object,
                             Template)
from utils.ndf import ensure
from utils.ndf.decorators import ndf_path
from utils.types.message import Message

from model.template_infantry_selector_tactic import \
    TemplateInfantrySelectorTactic

if TYPE_CHECKING:
    from context.mod_creation import ModCreationContext


def _mesh_alternative(index: int) -> str:
    return f"'MeshAlternative_{index}'"

class InfantryUnitCreator(UnitCreator):
    def __init__(self: Self,
                 ctx: ModCreationContext,
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 showroom_src: str | UnitMetadata | None = None,
                 button_texture_key: str | None = None,
                 msg: Message | None = None,
                 country: str | None = None,
                 *weapons: tuple[InfantryWeapon, int]):
        super().__init__(ctx, localized_name, new_unit, src_unit, showroom_src, button_texture_key, msg)
        self.country = country
        self.weapon_set = InfantryWeaponSet(*weapons)
        self._keys = _SquadKeys(self.new_unit)
        self._cached_weapon_assignment: dict[int, list[int]] | None = None

    @staticmethod
    def copy_parent(guids: GuidManager, creator: UnitCreator, country: str, *weapons: tuple[InfantryWeapon, int]):
        return InfantryUnitCreator(guids, creator, country, None, *weapons)

    # properties

    @property
    def soldier_count(self: Self) -> int:
        return self.weapon_set.soldier_count

    @property
    def _infantry_squad_weapon_assignment(self: Self) -> Object:
        if self._cached_weapon_assignment is None:
            self._cached_weapon_assignment = self.weapon_set.assignment
        return ensure._object('TInfantrySquadWeaponAssignmentModuleDescriptor',
                               InitialSoldiersToTurretIndexMap=self._cached_weapon_assignment)
    
    # internal methods

    def _gfx(self: Self) -> Object:
        return ensure._object('TemplateInfantryDepictionSquad',
                              SoundOperator=f'$/GFX/Sound/DepictionOperator_MovementSound_SM_Infanterie_{ensure.unquoted(ensure.country_sound_code(self.country), "'")}')    
    
    def _all_weapon_alternatives(self: Self) -> List:
        result = List()
        for weapon in self.weapon_set:
            result.add(ListRow(ensure._object('TDepictionDescriptor',
                                              SelectorId=[_mesh_alternative(weapon.art_index)],
                                              MeshDescriptor=weapon.model_path)))
        result.add(ListRow(ensure._object('TMeshlessDepictionDescriptor',
                                          SelectorId=["'none'"],
                                          ReferenceMeshForSkeleton=self.weapon_set.last.model_path)))
        return result
    
    def _all_weapon_sub_depiction(self: Self) -> Object:
        operators = List()
        for weapon in self.weapon_set:
            operators.add(ensure.listrow(ensure._object(
                'DepictionOperator_WeaponInstantFireInfantry',
                FireEffectTag=[weapon.effect_tag],
                WeaponShootDataPropertyName=f'"WeaponShootData_0_{weapon.art_index}"'
            )))
        return ensure._object('TemplateAllSubWeaponDepiction',
                                Alternatives=self._keys._all_weapon_alternatives,
                                Operators=operators)
    
    def _all_weapon_sub_depiction_backpack(self: Self) -> Object:
        return ensure._object('TemplateAllSubBackpackWeaponDepiction',
                                Alternatives=self._keys._all_weapon_alternatives)

    def _conditional_tags(self: Self) -> List:
        result = List()
        for weapon in self.weapon_set:
            if weapon.type is not None:
                result.add(ensure.listrow((weapon.type, _mesh_alternative(weapon.index))))
        return result

    def _tactic_depiction_soldier(self: Self, selector_tactic: TemplateInfantrySelectorTactic) -> Object:
        return ensure._object('TemplateInfantryDepictionFactoryTactic',
                                Selector=selector_tactic.name,
                                Alternatives=self._keys._tactic_depiction_alternatives,
                                SubDepictions=[self._keys._all_weapon_sub_depiction, self._keys._all_weapon_sub_depiction_backpack],
                                Operators=ensure._list(ensure._object('DepictionOperator_SkeletalAnimation2_Default', ConditionalTags=self._conditional_tags())))
    
    def _tactic_depiction_ghost(self: Self, selector_tactic: TemplateInfantrySelectorTactic) -> Object:
        return ensure._object('TemplateInfantryDepictionFactoryGhost',
                                Selector=selector_tactic.name,
                                Alternatives=self._keys._tactic_depiction_alternatives)

    @ndf_path(ndf_paths.GENERATED_DEPICTION_INFANTRY)
    def edit_generated_depiction_infantry(self: Self, ndf: List) -> None:
        ndf.add(ListRow(self._gfx(), namespace=f'Gfx_{self.new_unit.name}'))
        ndf.add(ListRow(self._all_weapon_alternatives(), namespace=self._keys._all_weapon_alternatives))
        ndf.add(ListRow(self._all_weapon_sub_depiction(), namespace=self._keys._all_weapon_sub_depiction))
        ndf.add(ListRow(self._all_weapon_sub_depiction_backpack(), namespace=self._keys._all_weapon_sub_depiction_backpack))
        tactic_depiction: List = ndf.by_name(ensure.prefix_and_suffix(self.src_unit.name, 'TacticDepiction_', '_Alternatives')).value.copy()        
        ndf.add(ListRow(tactic_depiction, namespace=self._keys._tactic_depiction_alternatives))
        selector_tactic: TemplateInfantrySelectorTactic\
            = TemplateInfantrySelectorTactic.from_tuple(ndf.by_name('TransportedInfantryAlternativesCount').value\
                                                           .by_key(self.src_unit.quoted_name).value)
        ndf.add(ListRow(self._tactic_depiction_soldier(selector_tactic), namespace=self._keys._tactic_depiction_soldier))
        ndf.add(ListRow(self._tactic_depiction_ghost(selector_tactic), namespace=self._keys._tactic_depiction_ghost))
        ndf.by_name('InfantryMimetic').value.add(MapRow(key=self._keys._unit, value=self._keys._tactic_depiction_soldier))
        ndf.by_name('InfantryMimeticGhost').value.add(MapRow(key=self._keys._unit, value=self._keys._tactic_depiction_ghost))
        ndf.by_name('TransportedInfantryAlternativesCount').value.add(ensure.maprow(self._keys._unit,
                                                                                    selector_tactic.tuple))
        
    def apply(self: Self) -> None:
        self.edit_unit()
        super().apply()
        self.edit_generated_depiction_infantry(self.ndf, self.msg)
        self.edit_showroom_units(self.ndf, self.msg)
        self.edit_weapon_descriptors(self.ndf, self.msg)

    def _make_infantry_squad_module_descriptor(self: Self, guid_key: str) -> Object:
        return ensure._object('TInfantrySquadModuleDescriptor',
                              NbSoldatInGroupeCombat=self.soldier_count,
                              InfantryMimeticName=self._keys._unit,
                              WeaponUnitFXKey=self._keys._unit,
                              MimeticDescriptor=ensure._object('Descriptor_Unit_MimeticUnit', 
                                                               DescriptorId=self.ctx.guids.generate(guid_key),
                                                               MimeticName=self._keys._unit),
                              BoundingBoxSize=f'{self.soldier_count + 2} * Metre')

    def _edit_groupe_combat(self: Self, module: Object) -> None:
        edit.members(module,
                     Default=self._make_infantry_squad_module_descriptor(f'{self.new_unit.descriptor_name}/ModulesDescriptors["GroupeCombat"]/Default/MimeticDescriptor'))
        
    @ndf_path(ndf_paths.SHOWROOM_UNITS)
    def edit_showroom_units(self: Self, ndf: List):
        copy: Object = ndf.by_name(self.showroom_src.showroom_descriptor_name).value.copy()
        edit.members(copy,
                     DescriptorId=self.ctx.guids.generate(self.src_unit.showroom_descriptor_name))
        module.replace_where(copy, self.new_unit.weapon_descriptor_path, lambda x: isinstance(x.value, str) and x.value.startswith('$/GFX/Weapon/'))
        module.replace_module(copy,
                              self._make_infantry_squad_module_descriptor(module.path_by_type(self.src_unit.showroom_descriptor_name,
                                                                                             'TInfantrySquadModuleDescriptor',
                                                                                             'MimeticDescriptor',
                                                                                             'DescriptorId')),
                              'TInfantrySquadModuleDescriptor')
        module.replace_module(copy,
                              self._infantry_squad_weapon_assignment,
                              'TInfantrySquadWeaponAssignmentModuleDescriptor')
        ndf.add(ListRow(copy, 'export', self.new_unit.showroom_descriptor_name))
        
    @ndf_path(ndf_paths.WEAPON_DESCRIPTOR)
    def edit_weapon_descriptors(self: Self, ndf: List):
        ndf.add(ListRow(self.weapon_set.to_weapon_descriptor(), 'export', self.new_unit.weapon_descriptor_name))
    
    def edit_unit(self: Self) -> None:
        self.edit_module_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=self.soldier_count)        
        self._edit_groupe_combat(self.get_module('GroupeCombat', by_name=True))
        self.replace_module('TInfantrySquadWeaponAssignmentModuleDescriptor', self._infantry_squad_weapon_assignment)
        self.edit_module_members('TTacticalLabelModuleDescriptor', NbSoldiers=self.soldier_count)
        self.edit_module_members('WeaponManager', by_name=True, Default=self.new_unit.weapon_descriptor_path)
        # this should edit showroomequivalence when the unit is saved
        self.showroom_src = self.new_unit