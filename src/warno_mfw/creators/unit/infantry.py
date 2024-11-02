from typing import Self

import warno_mfw.constants.ndf_paths as ndf_paths
# import warno_mfw.context.mod_creation as ctx
import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.unit_module as module
from warno_mfw.constants import ndf_paths
from warno_mfw.constants.enums import country_sound_code
from warno_mfw.creators.unit.abc import UnitCreator
from warno_mfw.creators.unit.basic import BasicUnitCreator
from warno_mfw.creators.unit.utils.infantry._squad_keys import _SquadKeys
from warno_mfw.creators.unit.utils.infantry.weapon import InfantryWeapon
from warno_mfw.creators.unit.utils.infantry.weapon_set import InfantryWeaponSet
from warno_mfw.managers.guid import GuidManager
from warno_mfw.metadata.unit import UnitMetadata
from warno_mfw.model.template_infantry_selector_tactic import \
    TemplateInfantrySelectorTactic
from warno_mfw.utils.ndf import ensure
from warno_mfw.utils.ndf.decorators import ndf_path
from warno_mfw.utils.types.message import Message
from ndf_parse.model import List, ListRow, Map, MapRow, Object


def _mesh_alternative(index: int) -> str:
    return f"'MeshAlternative_{index}'"

class InfantryUnitCreator(UnitCreator):
    def __init__(self: Self,
                 ctx,# : ctx.ModCreationContext,
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 button_texture: str | None = None,
                 msg: Message | None = None,
                 country: str | None = None,
                 *weapons: tuple[InfantryWeapon, int]):
        super().__init__(ctx, localized_name, new_unit, src_unit, button_texture, msg)
        self.country = country
        self.weapon_set = InfantryWeaponSet(*weapons)
        self._keys = _SquadKeys(self.new_unit)
        self._cached_weapon_assignment: dict[int, list[int]] | None = None

    # overrides
    
    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new_unit.descriptor.path, v=self.new_unit.descriptor.showroom.path)

    def post_apply(self: Self, msg: Message) -> None:
        self.edit_generated_depiction_infantry(self.ndf, msg)
        self._edit_showroom_units(self.ndf, msg)
        self.edit_showroom_equivalence(self.ndf, msg)
        self.edit_weapon_descriptors(self.ndf, msg)
        self.edit_unit()

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
                              SoundOperator=f'$/GFX/Sound/DepictionOperator_MovementSound_SM_Infanterie_{ensure.unquoted(country_sound_code(self.country), "'")}')    
    
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

    def _make_infantry_squad_module_descriptor(self: Self, guid_key: str) -> Object:
        return ensure._object('TInfantrySquadModuleDescriptor',
                              NbSoldatInGroupeCombat=self.soldier_count,
                              InfantryMimeticName=self._keys._unit,
                              WeaponUnitFXKey=self._keys._unit,
                              MimeticDescriptor=ensure._object('Descriptor_Unit_MimeticUnit', 
                                                               DescriptorId=self.ctx.guids.generate(guid_key),
                                                               MimeticName=self._keys._unit))

    def _edit_groupe_combat(self: Self, module: Object) -> None:
        edit.members(module,
                     Default=self._make_infantry_squad_module_descriptor(f'{self.new_unit.descriptor.name}/ModulesDescriptors["GroupeCombat"]/Default/MimeticDescriptor'))
        
    @ndf_path(ndf_paths.SHOWROOM_UNITS)
    def _edit_showroom_units(self: Self, ndf: List):
        copy: Object = ndf.by_name(self.src_unit.descriptor.showroom.name).value.copy()
        edit.members(copy,
                     DescriptorId=self.ctx.guids.generate(self.src_unit.descriptor.showroom.name))
        module.replace_where(copy, self.new_unit.weapon_descriptor.path, lambda x: isinstance(x.value, str) and x.value.startswith('$/GFX/Weapon/'))
        module.replace(copy,
                              self._make_infantry_squad_module_descriptor(module.path_by_type(self.src_unit.descriptor.showroom.name,
                                                                                             'TInfantrySquadModuleDescriptor',
                                                                                             'MimeticDescriptor',
                                                                                             'DescriptorId')),
                              'TInfantrySquadModuleDescriptor')
        module.replace(copy,
                              self._infantry_squad_weapon_assignment,
                              'TInfantrySquadWeaponAssignmentModuleDescriptor')
        ndf.add(ListRow(copy, 'export', self.new_unit.descriptor.showroom.name))
        
    @ndf_path(ndf_paths.WEAPON_DESCRIPTOR)
    def edit_weapon_descriptors(self: Self, ndf: List):
        ndf.add(ListRow(self.weapon_set.to_weapon_descriptor(), 'export', self.new_unit.weapon_descriptor.name))
    
    def edit_unit(self: Self) -> None:
        self.modules.edit_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=self.soldier_count)        
        self._edit_groupe_combat(self.unit.modules.get('GroupeCombat', by_name=True))
        self.modules.replace('TInfantrySquadWeaponAssignmentModuleDescriptor', self._infantry_squad_weapon_assignment)
        self.modules.edit_members('TTacticalLabelModuleDescriptor', NbSoldiers=self.soldier_count)
        self.modules.edit_members('WeaponManager', by_name=True, Default=self.new_unit.weapon_descriptor.path)