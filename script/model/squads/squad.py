from typing import Self

from model.squads.infantry_weapon_set import InfantryWeaponSet
from creators.unit import UnitCreator
from context.module_context import ModuleContext
from script.context.mod_creation_context import ModCreationContext
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from constants import ndf_paths
from managers.guid import GuidManager
from metadata.unit import UnitMetadata
from model.squads._utils import (COUNTRY_CODE_TO_COUNTRY_SOUND_CODE,
                                 mesh_alternative)
from model.squads.template_infantry_selector_tactic import \
    TemplateInfantrySelectorTactic
from model.squads.weapon import Weapon, WeaponWithIndex
from ndf_parse.model import (List, ListRow, Map, MapRow, MemberRow, Object,
                             Template)
from utils.collections import flatten, unique, with_indices
from utils.ndf import ensure
from utils.ndf.decorators import ndf_path
from utils.types.message import Message
import constants.ndf_paths as ndf_paths


class Squad(object):
    def __init__(self: Self,
                 guids: GuidManager,
                 metadata: UnitMetadata,
                 country: str,
                 infantry_selector_tactic: TemplateInfantrySelectorTactic | tuple[int | str, int | str],
                 tactic_depiction: str | List,
                 weapon_set: InfantryWeaponSet,
                 *loadout: WeaponWithIndex | list[WeaponWithIndex] | tuple[int, list[WeaponWithIndex]]):
        self.guids = guids
        self.metadata = metadata
        self.country = country
        if isinstance(infantry_selector_tactic, tuple):
            infantry_selector_tactic = TemplateInfantrySelectorTactic.from_tuple(infantry_selector_tactic)
        self.infantry_selector_tactic = infantry_selector_tactic
        if isinstance(tactic_depiction, str):
            tactic_depiction = ensure.prefix_and_suffix(tactic_depiction, 'TacticDepiction_', '_Alternatives')
        self.tactic_depiction = tactic_depiction
        self.weapon_set = weapon_set
        self.loadout: list[list[Weapon]] = []
        for item in loadout:
            if isinstance(item, Weapon):
                item = [item]
            if isinstance(item, list):
                item = (1, item)
            ct, weapons = item
            for _ in range(ct):
                self.loadout.append(weapons)

    @staticmethod
    def copy(ctx: ModCreationContext,
             metadata: UnitMetadata,
             country: str,
             copy_of: str,
             weapon_set: InfantryWeaponSet,
             *precedence: int | list[int]):
        return Squad(ctx.guids,
                     metadata,
                     country,
                     ctx.ndf[ndf_paths.GENERATED_DEPICTION_INFANTRY]
                        .by_name('TransportedInfantryAlternativesCount').value
                        .by_key(ensure.quoted(copy_of).value),
                     ctx.ndf[ndf_paths.GENERATED_DEPICTION_INFANTRY]
                        .by_name(ensure.prefix_and_suffix(copy_of, 'TacticDepiction_', '_Alternatives').value),
                     weapon_set,
                     ... # TODO: aaaaaaaaaaaaaaaaaa
                     )

    @staticmethod
    def from_weapon_set(guids: GuidManager,
                        metadata: UnitMetadata,
                        country: str,
                        infantry_selector_tactic: TemplateInfantrySelectorTactic | tuple[int, int],
                        tactic_depiction: str | List,
                        weapons: InfantryWeaponSet,
                        has_at_weapon: bool = True) -> Self:
        """ Assumes a standard infantry loadout. TODO: describe what that means """
        loadout: list[tuple[int, list[WeaponWithIndex]]] = []
        ct = len(weapons.count) if not has_at_weapon else len(weapons.count) - 1
        order = [weapons.count - i - 1 for i in range(ct)]
        if has_at_weapon: order.append(weapons.count - 1)
        for i in order:
            loadout.append((weapons.counts[i], weapons.weapons[i]))
        return Squad(guids,
                     metadata,
                     country,
                     infantry_selector_tactic,
                     tactic_depiction,
                     *loadout)

    # properties

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
    def key(self: Self) -> str:
        return self.metadata.class_name_for_debug

    @property
    def tactic_depiction_alternatives_key(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Alternatives'

    @property
    def tactic_depiction_soldier_key(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Soldier'
    
    @property
    def tactic_depiction_ghost_key(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Ghost'

    @property
    def total_soldiers(self: Self) -> int:
        return len(self.loadout)
    
    @property
    def unique_weapons_with_indices(self: Self) -> list[tuple[int, Weapon]]:
        return [with_indices([x for x in unique(flatten(self.loadout))], 1)]
    
    # internal methods

    def _gfx(self: Self) -> Object:
        return ensure._object('TemplateInfantryDepictionSquad',
                              SoundOperator=f'$/GFX/Sound/DepictionOperator_MovementSound_SM_Infanterie_{COUNTRY_CODE_TO_COUNTRY_SOUND_CODE[self.country]}')    
    
    def _all_weapon_alternatives(self: Self) -> List:
        result = List()
        unique_weapons = self.unique_weapons_with_indices
        for index, item in unique_weapons:
            result.add(ListRow(ensure._object(SelectorId=[mesh_alternative(index)],
                                              MeshDescriptor=item.model_path)))
        result.add(ListRow(ensure._object(SelectorId="'none'", ReferenceMeshForSkeleton=unique_weapons[-1][1].model_path)))
        return result
    
    def _all_weapon_sub_depiction(self: Self):
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
    
    def _all_weapon_sub_depiction_backpack(self: Self) -> Template:
        return ensure._template('TemplateAllSubBackpackWeaponDepiction',
                                Alternatives=self.all_weapon_sub_depiction_key)

    def _conditional_tags(self: Self) -> List:
        result = List()
        for index, weapon in self.unique_weapons_with_indices:
            if weapon.weapon_type is not None:
                result.add(ensure.memberrow(weapon.weapon_type, mesh_alternative(index)))
        return result

    def _tactic_depiction_soldier(self: Self) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryTactic',
                                Selector=self.infantry_selector_tactic.name,
                                Alternatives=self.tactic_depiction_alternatives_key,
                                SubDepictions=[self.all_weapon_sub_depiction_key, self.all_weapon_sub_depiction_backpack_key],
                                Operators=ensure._object('DepictionOperator_SkeletalAnimation2_Default', ConditionalTags=self._conditional_tags()))
    
    def _tactic_depiction_ghost(self: Self) -> Template:
        return ensure._template('TemplateInfantryDepictionFactoryGhost',
                                Selector=self.infantry_selector_tactic.name,
                                Alternatives=self.tactic_depiction_alternatives_key)

    @ndf_path(ndf_paths.GENERATED_DEPICTION_INFANTRY)
    def edit_generated_depiction_infantry(self: Self, ndf: List) -> None:
        ndf.add(ListRow(self._gfx(), namespace=f'Gfx_{self.metadata.name}'))
        ndf.add(ListRow(self._all_weapon_alternatives(), namespace=self.all_weapon_alternatives_key))
        ndf.add(ListRow(self._all_weapon_sub_depiction(), namespace=self.all_weapon_sub_depiction_key))
        ndf.add(ListRow(self._all_weapon_sub_depiction_backpack(), namespace=self.all_weapon_sub_depiction_backpack_key))
        if isinstance(self.tactic_depiction, str):
            self.tactic_depiction = ndf.by_name(self.tactic_depiction).value
        ndf.add(ListRow(self.tactic_depiction.copy(), namespace=self.tactic_depiction_alternatives_key))
        ndf.add(ListRow(self._tactic_depiction_soldier(), self.tactic_depiction_soldier_key))
        ndf.add(ListRow(self._tactic_depiction_ghost(), self.tactic_depiction_ghost_key))
        ndf.by_name('InfantryMimetic').value.add(MapRow(key=self.key, value=self.tactic_depiction_soldier_key))
        ndf.by_name('InfantryMimeticGhost').value.add(MapRow(key=self.key, value=self.tactic_depiction_ghost_key))
        ndf.by_name('TransportedInfantryAlternativesCount').value.add(ensure.maprow(self.key,
                                                                                    self.infantry_selector_tactic.tuple))
        
    def apply(self: Self, ndf: dict[str, List], msg: Message | None) -> None:
        self.edit_generated_depiction_infantry(ndf, msg)

    def _make_infantry_squad_module_descriptor(self: Self, guid_key: str) -> Object:
        return ensure._object('TInfantrySquadModuleDescriptor',
                              NbSoldatInGroupeCombat=self.total_soldiers,
                              InfantryMimeticName=self.key,
                              WeaponUnitFXKey=self.key,
                              MimeticDescriptor=ensure._object('Descriptor_Unit_MimeticUnit', 
                                                               DescriptorId=self.guids.generate(guid_key),
                                                               MimeticName=self.key),
                              BoundingBoxSize=f'{self.total_soldiers + 2} * Metre')

    def _edit_groupe_combat(self: Self, module: Object) -> None:
        edit.members(module, Default=self._make_infantry_squad_module_descriptor(f'{self.metadata.descriptor_name}/ModulesDescriptors["GroupeCombat"]/Default/MimeticDescriptor'))
        
    def _create_infantry_squad_weapon_assignment(self: Self) -> Object:
        turret_map: dict[int, list[int]] = {}
        for i in range(len(self.loadout)):
            turret_map[i] = [w.index for w in self.loadout[i]]
        return ensure._object('TInfantrySquadWeaponAssignmentModuleDescriptor',
                              InitialSoldiersToTurretIndexMap=turret_map)
    
    def _create_showroom_unit(self: Self, copy_of: UnitMetadata, ndf: dict[str, List], assignment_module: Object) -> Object:
        showroom_units = ndf[ndf_paths.SHOWROOM_UNITS]
        copy: Object = showroom_units.by_name(copy_of.showroom_descriptor_name).value.copy()
        edit.members(copy,
                     DescriptorId=self.guids.generate(copy_of.showroom_descriptor_name))
        # TODO: find member pointing at a weapondescriptor and point it at ours instead
        module.replace_where(copy, self.metadata.weapon_descriptor_path, lambda x: x.value.startswith('$/GFX/Weapon/'))
        module.replace_module(copy,
                              self._make_infantry_squad_module_descriptor(f'{copy_of.showroom_descriptor_name}/ModulesDescriptors[TInfantrySquadModuleDescriptor]/MimeticDescriptor'),
                              'TInfantrySquadModuleDescriptor')
        module.replace_module(copy,
                              assignment_module.copy(),
                              'TInfantrySquadWeaponAssignmentModuleDescriptor')
        
    @ndf_path(ndf_paths.WEAPON_DESCRIPTOR)
    def edit_weapon_descriptors(self: Self, ndf: List):
        pass
    
    def edit_unit(self: Self, unit: UnitCreator) -> None:
        unit.edit_module_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=self.total_soldiers)        
        self._edit_groupe_combat(unit.get_module('GroupeCombat', by_name=True))
        unit.replace_module(self._create_infantry_squad_weapon_assignment(), 'TInfantrySquadWeaponAssignmentModuleDescriptor')
        unit.edit_module_members('TTacticalLabelModuleDescriptor', NbSoldiers=self.total_soldiers)
        unit.edit_module_members('WeaponManager', by_name=True, Default=self.metadata.weapon_descriptor_path)