from copy import deepcopy
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
from model.t_depiction_descriptor import TDepictionDescriptor
from model.template_infantry_selector_tactic import \
    TemplateInfantrySelectorTactic
from ndf_parse.model import (List, ListRow, Map, MapRow, MemberRow, Object,
                             Template)
from utils.ndf import ensure
from utils.ndf.decorators import ndf_path
from utils.types.message import Message

if TYPE_CHECKING:
    from context.mod_creation import ModCreationContext


def _mesh_alternative(index: int) -> str:
    return f"'MeshAlternative_{index}'"

class TowedUnitCreator(UnitCreator):
    def __init__(self: Self,
                 ctx,#: ModCreationContext,
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 gfx_src_unit: str | UnitMetadata | None = None,
                 button_texture_key: str | None = None,
                 msg: Message | None = None,
                 country: str | None = None,
                 *servants: tuple[str, str]):
        super().__init__(ctx, localized_name, new_unit, src_unit, gfx_src_unit, button_texture_key, msg)
        self.country = country
        self.servants = servants
        self._keys = _SquadKeys(self.new_unit)
        self._cached_weapon_assignment: dict[int, list[int]] | None = None

    @staticmethod
    def copy_parent(guids: GuidManager, creator: UnitCreator, country: str, *weapons: tuple[InfantryWeapon, int]):
        return TowedUnitCreator(guids, creator, country, None, *weapons)

    def apply(self: Self) -> None:
        # hacky fix but fuck it
        # should maybe make an abc idk
        showroom_src = self.showroom_src
        self.showroom_src = self.new_unit
        super().apply()
        self.showroom_src = showroom_src
        self.edit_generated_depiction_infantry(self.ndf, self.msg)
        self.edit_showroom_units(self.ndf, self.msg)
        self.edit_weapon_descriptors(self.ndf, self.msg)
        self.edit_unit()

    # properties
    
    # internal methods:
    #   edit ApparenceModel to point to:
    #       - new depiction
    #       - existing [rest] from copied unit    
    def edit_unit(self: Self) -> None:
        self.edit_module_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=self.soldier_count)
    #   edit Gfx/Depictions/GeneratedTowable.ndf:
    #       - copy Alternatives values to new key
    #       - ditto InitialPoses
    #       - if has missiles, ditto MissileAlternatives and AllowedUnits
    @ndf_path(ndf_paths.GENERATED_TOWABLE)
    def _edit_generated_towable(self: Self, ndf: List) -> None:
        sub_depiction_towed_unit: Object = ndf.by_name('SubDepictionTowedUnit').value
        alternatives: List = sub_depiction_towed_unit.by_member('Alternatives').value
        alternatives_py: list[TDepictionDescriptor] = [TDepictionDescriptor.from_ndf(x) for x in alternatives]
        for alternative in alternatives_py:
            if alternative.SelectorId[1] == self.src_unit.quoted_name:
                copy = deepcopy(alternative)
                copy.SelectorId[1] = self.new_unit.quoted_name
                alternatives.add(copy.to_ndf())
        initial_poses: Map = sub_depiction_towed_unit.by_member('InitialPoses').value
        initial_pose = initial_poses.by_key(self.src_unit.quoted_name)
        initial_poses.add(self.new_unit.quoted_name, initial_pose.copy())
        # TODO: the 'if has missiles' case above

    #   edit GeneratedDepictionHumans:
    #       - copy originals
    #       - if custom servants specified, apply these changes

    @ndf_path(ndf_paths.GENERATED_DEPICTION_HUMANS)
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
        
    #   edit GeneratedDepictionVehicles:
    #       - ~~copy existing DepictionOperators~~ (actually, should be fine leaving these)
    #       - copy Gfx, changing onlky SubDepictions to change to HumanSubDepictions
    #   edit GeneratedDepictionVehiclesShowroom:
    #       - make new, pointing to custom Alternatives, Selector, and HumanSubDepictions
    #   edit ShowroomUnits:
    #       - copy src
    #       - give it new guid
    #       - replace gfx path
    #       - replace TApparenceModuleDescriptor
        
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