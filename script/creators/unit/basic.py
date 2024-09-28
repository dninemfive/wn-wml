from typing import TYPE_CHECKING, Callable, Self

import constants.ndf_paths as ndf_paths
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
from context.unit_module import UnitModuleContext
from creators.weapon import WeaponCreator
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Map, MemberRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf.decorators import ndf_path
from utils.types.message import Message

if TYPE_CHECKING:
    from context.mod_creation import ModCreationContext

MODULES_DESCRIPTORS = "ModulesDescriptors"
UNIT_UI = "TUnitUIModuleDescriptor"
TAGS = "TTagsModuleDescriptor"

class UnitCreator(object):
    def __init__(self: Self,
                 ctx: ModCreationContext,
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 showroom_src: str | UnitMetadata | None = None,
                 button_texture_key: str | None = None,
                 msg: Message | None = None):
        self.ctx = ctx
        self.localized_name = localized_name
        self.new_unit: UnitMetadata = UnitMetadata.resolve(new_unit)
        self.src_unit: UnitMetadata = UnitMetadata.resolve(src_unit)
        self.showroom_src: UnitMetadata = UnitMetadata.try_resolve(showroom_src, src_unit)
        self.button_texture_key = button_texture_key
        self.msg = msg

    def __enter__(self: Self) -> Self:
        self.msg = self.msg.nest(f"Making {self.localized_name}")
        self.msg.__enter__()
        with self.msg.nest(f"Copying {self.src_unit.descriptor_name}") as _:
            self.unit_object = self.make_copy()
        self.edit_ui_module(NameToken=self.ctx.localization.register(self.localized_name))
        if self.button_texture_key is not None:
            self.edit_ui_module(ButtonTexture=self.button_texture_key)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.remove(tag_set.find_by_cond(lambda x: x.value == self.src_unit.tag))
            tag_set.add(ListRow(self.new_unit.tag))
        try:
            with self.module_context("TTransportableModuleDescriptor") as transportable_module:
                transportable_module.edit_members(TransportedSoldier=f'"{self.new_unit.name}"')
        except:
            pass
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.apply()
        self.msg.__exit__(exc_type, exc_value, traceback)

    def apply(self: Self):
        with self.msg.nest(f"Saving {self.new_unit.name}") as msg2:
            self.edit_unite_descriptor(self.ndf, msg2)
            self.edit_division_packs(self.ndf, msg2)
            self.edit_showroom_equivalence(self.ndf, msg2)
            self.edit_all_units_tactic(self.ndf, msg2)

    def make_copy(self: Self) -> Object:
        copy: Object = self.ndf[ndf_paths.UNITE_DESCRIPTOR].by_name(self.src_unit.descriptor_name).value.copy()
        edit.members(copy,
                     DescriptorId=self.ctx.guids.generate(self.new_unit.descriptor_name),
                     ClassNameForDebug=self.new_unit.class_name_for_debug)
        return copy
    
    @property
    def ndf(self: Self) -> dict[str, List]:
        return self.ctx.ndf

    @ndf_path(ndf_paths.UNITE_DESCRIPTOR)
    def edit_unite_descriptor(self: Self, ndf: List):
        ndf.add(ListRow(self.unit_object, namespace=self.new_unit.descriptor_name, visibility="export"))

    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new_unit.descriptor_path, v=self.showroom_src.showroom_descriptor_path)

    @ndf_path(ndf_paths.DIVISION_PACKS)
    def edit_division_packs(self: Self, ndf: List):
        deck_pack_descriptor = Object('DeckPackDescriptor')
        deck_pack_descriptor.add(MemberRow(self.new_unit.descriptor_path, "Unit"))
        ndf.add(ListRow(deck_pack_descriptor, namespace=self.new_unit.deck_pack_descriptor_name))

    @ndf_path(ndf_paths.ALL_UNITS_TACTIC)
    def edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.new_unit.descriptor_path)

    def edit_weapons(self: Self, copy_of: str | None = None) -> WeaponCreator:
        if copy_of is None:
            copy_of = self.src_unit.name
        def _set_weapon_descriptor(descriptor_name: str) -> None:
            with self.module_context('WeaponManager', by_name=True) as ctx:
                ctx.edit_members(Default=ensure.prefix(descriptor_name, '$/GFX/Weapon/'))
        return WeaponCreator(self.ndf, self.new_unit, copy_of, self.msg, _set_weapon_descriptor)

    def module_context(self: Self, type_or_name: str, by_name: bool = False) -> UnitModuleContext:
        return UnitModuleContext(self.unit_object, type_or_name, by_name)
    
    def edit_ui_module(self: Self, **changes: CellValue) -> None:
        with self.module_context(UNIT_UI) as ui_module:
            ui_module.edit_members(**changes)

    def set_name(self: Self, name: str) -> None:
        self.edit_ui_module(NameToken=self.ctx.localization.register(name))

    @property
    def LocalizedName(self: Self) -> str:
        return self.localized_name
    
    @LocalizedName.setter
    def LocalizedName(self: Self, val: str) -> None:
        self.localized_name = val
        self.edit_ui_module(NameToken=self.ctx.localization.register(val))

    def add_tag(self: Self, tag: str) -> None:
        tag = ensure.quoted(tag)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.add(tag)
    
    def add_tags(self: Self, *tags: str) -> None:
        for tag in tags:
            self.add_tag(tag)

    def remove_tag(self: Self, tag: str) -> None:
        tag = ensure.quoted(tag)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            index = tag_set.find_by_cond(lambda x: x.value == tag)
            tag_set.remove(index)

    def remove_tags(self: Self, *tags: str) -> None:
        for tag in tags:
            self.remove_tag(tag)

    # modules

    def get_module_index(self: Self, type_or_name: str, by_name: bool = False) -> int:
        return modules.get_index(self.unit_object, type_or_name, by_name)
    
    def get_module(self: Self, type_or_name: str, by_name: bool = False) -> Object:
        return modules.get(self.unit_object, type_or_name, by_name)
    
    def get_module_row(self: Self, type_or_name: str, by_name: bool = False) -> ListRow:
        return modules.get_row(self.unit_object, type_or_name, by_name)
    
    def replace_module(self: Self, type_or_name: str, module: CellValue, by_name: bool = False):
        return modules.replace_module(self.unit_object, module, type_or_name, by_name)
    
    def replace_module_from(self: Self, other_unit: str | Object, type_or_name: str, by_name: bool = False) -> None:
        if isinstance(other_unit, str):
            other_unit = self.get_other_unit(ensure.unit_descriptor(other_unit))
        return modules.replace_from(self.unit_object, other_unit, type_or_name, by_name)
    
    def append_module(self: Self, module: Object | ListRow):
        return modules.append(self.unit_object, module)
    
    def remove_module(self: Self, type_or_name: str, by_name: bool = False):
        return modules.remove(self.unit_object, type_or_name, by_name)
    
    def remove_module_where(self: Self, predicate: Callable[[ListRow], bool]):
        return modules.remove_where(self.unit_object, predicate)
    
    def append_module_from(self: Self, other_unit: Object, type_or_name: str, by_name: bool = False):
        return modules.append_from(self.unit_object, other_unit, type_or_name, by_name)
    
    def edit_module_members(self: Self, module: str, by_name: bool = False, **changes: CellValue | None):
        edit.members(self.get_module(module, by_name), **changes)
    
    def get_other_unit(self: Self, unit: str) -> Object:
        return self.ndf[ndf_paths.UNITE_DESCRIPTOR].by_name(ensure.unit_descriptor(unit)).value
    
    @property
    def UpgradeFromUnit(self: Self) -> str:
        return self.get_module(UNIT_UI).by_member('UpgradeFromUnit').value

    @UpgradeFromUnit.setter
    def UpgradeFromUnit(self: Self, val: str | None) -> None:
        if val is None:
            with self.module_context(UNIT_UI) as ctx:
                ctx.remove_member('UpgradeFromUnit')
        else: 
            self.edit_ui_module(UpgradeFromUnit=ensure.prefix(val, 'Descriptor_Unit_'))

    @property
    def CommandPointCost(self: Self) -> int:
        return int(self.get_module('TProductionModuleDescriptor')
                       .by_member('ProductionRessourcesNeeded').value
                       .by_key('$/GFX/Resources/Resource_CommandPoints').value)
    
    @CommandPointCost.setter
    def CommandPointCost(self: Self, val: int) -> None:
        with self.module_context('TProductionModuleDescriptor') as context:
            context.object.by_member('ProductionRessourcesNeeded').value\
                          .by_key('$/GFX/Resources/Resource_CommandPoints').value = val
            
    @property
    def MotherCountry(self: Self) -> str:
        unit_type_module: Object = self.get_module('TTypeUnitModuleDescriptor')
        return ensure.unquoted(unit_type_module.by_member('MotherCountry').value, "'")

    @MotherCountry.setter
    def MotherCountry(self: Self, val: str) -> None:
        with self.module_context("TTypeUnitModuleDescriptor") as unit_type_module:
            unit_type_module.edit_members(MotherCountry=ensure.quoted(val, "'"))
        with self.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.edit_members(CountryTexture=f"'CommonTexture_MotherCountryFlag_{ensure.unquoted(val, "'")}'")

    @property
    def Factory(self: Self) -> str:
        return self.get_module('TProductionModuleDescriptor').by_member('Factory').value
    
    @Factory.setter
    def Factory(self: Self, val: str) -> None:
        edit.members(self.get_module('TProductionModuleDescriptor'), Factory=ensure.prefix(val, 'EDefaultFactories/'))