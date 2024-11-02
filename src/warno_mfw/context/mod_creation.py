from __future__ import annotations

from typing import Any, Self

import warno_mfw.constants.misc                               as cnst
import warno_mfw.constants.ndf_paths                          as ndf_paths
import warno_mfw.constants.paths                              as paths
import warno_mfw.creators.ammo                                as ca
import warno_mfw.creators.division                            as cd
import warno_mfw.creators.unit.basic                          as cub
import warno_mfw.creators.unit.infantry                       as cui
import warno_mfw.creators.unit.utils.infantry.weapon          as cuuiw
import warno_mfw.managers.guid                                as mg
import warno_mfw.managers.localization                        as ml
import warno_mfw.managers.unit_id                             as mu
import warno_mfw.metadata.division                            as med
import warno_mfw.metadata.mod                                 as mem
import warno_mfw.metadata.unit                                as meu
import warno_mfw.unit_registration.division_unit_registry     as reg
import warno_mfw.wrappers.unit                                as wu
from warno_mfw.utils.ndf import ensure
from warno_mfw.utils.ndf.files import add_image, add_image_literal
from warno_mfw.utils.types.cache import Cache
from warno_mfw.utils.types.message import Message, try_nest
from ndf_parse import Mod
from ndf_parse.model import List, Object
from ndf_parse.model.abc import CellValue

CACHES: list[tuple[str, type]] = [(cnst.GUID, str), (cnst.LOCALIZATION, str), (cnst.UNIT_ID, int)]

class ModCreationContext(object):
    @property
    def prefix(self: Self) -> str:
        return self.metadata.dev_short_name
    
    def __init__(self: Self, metadata: mem.ModMetadata, root_msg: Message | None, *ndf_paths: str):
        self.metadata = metadata
        self.mod = Mod(metadata.folder_path, metadata.folder_path)
        self.root_msg = root_msg
        self.paths = ndf_paths
        self.guid_cache:            Cache[str] = Cache(paths.CACHE_FOLDER, cnst.GUID)
        self.localization_cache:    Cache[str] = Cache(paths.CACHE_FOLDER, cnst.LOCALIZATION)
        self.unit_id_cache:         Cache[int] = Cache(paths.CACHE_FOLDER, cnst.UNIT_ID)
        self.guids = mg.GuidManager(self.guid_cache)
        self.localization = ml.LocalizationManager(self.localization_cache, self.metadata.localization_prefix)
       
    def __enter__(self: Self) -> Self:
        self.mod.check_if_src_is_newer()
        with try_nest(self.root_msg, "Loading ndf files") as msg:
            self.ndf = {x:self.load_ndf(x, msg) for x in sorted(self.paths)}
        self.load_caches()
        return self
    
    def load_ndf(self: Self, path: str, msg: Message) -> List:
        with msg.nest(f"Loading {path}") as _:
            return self.mod.edit(path).current_tree
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        success = exc_type is None and exc_value is None and traceback is None        
        if success:
            with self.root_msg.nest("Saving mod") as write_msg:
                self.write_edits(write_msg)
                self.generate_and_write_localization(write_msg)
            self.save_caches()
        else:
            pass # self.root_msg.fail()

    def load_caches(self: Self) -> None:
        with self.root_msg.nest("Loading caches...") as msg:
            for name, _ in CACHES:
                cache: Cache[Any] = getattr(self, f'{name}_cache')
                cache.load(msg)

    def save_caches(self: Self) -> None:
        with self.root_msg.nest("Saving caches...") as msg:
            for name, _ in CACHES:
                cache: Cache[Any] = getattr(self, f'{name}_cache')
                cache.save(msg)
    
    def create_division(self: Self,
                        division: med.DivisionMetadata,
                        copy_of: str,
                        units: reg.DivisionUnitRegistry,
                        insert_after: str | None = None,
                        root_msg: Message | None = None,
                        **changes: CellValue | None) -> None:
        with try_nest(root_msg, f"Making division {division.short_name}") as msg:
            cd.DivisionCreator(self.guids.generate(division.descriptor_name), copy_of, insert_after, division, units, **changes).apply(self.ndf, msg)

    def start_unit_ids_at(self: Self, initial_id: int) -> mu.UnitIdManager:
        return mu.UnitIdManager(self.unit_id_cache, initial_id)
    
    def create_unit(self: Self, name: str, country: str, copy_of: str, showroom_src: str | None = None, button_texture_src_path: str | None = None) -> cub.BasicUnitCreator:
        # TODO: msg here
        metadata: meu.UnitMetadata = meu.UnitMetadata.from_localized_name(self.prefix, name, country)
        return cub.BasicUnitCreator(self,
                                    name,
                                    metadata,
                                    copy_of,
                                    showroom_src,
                                    self.try_add_button_texture(button_texture_src_path, metadata),
                                    self.root_msg)
    
    def create_infantry_unit(self: Self,
                             name: str,
                             country: str,
                             copy_of: str,
                             weapons: list[tuple[cuuiw.InfantryWeapon, int]],
                             button_texture_src_path: str | None = None) -> cui.InfantryUnitCreator:
        metadata: meu.UnitMetadata = meu.UnitMetadata.from_localized_name(self.prefix, name, country)
        return cui.InfantryUnitCreator(self,
                                       name,
                                       metadata,
                                       copy_of,
                                       self.try_add_button_texture(button_texture_src_path, metadata),
                                       self.root_msg,
                                       country,
                                       *weapons)

    
    def add_division_emblem(self: Self, msg: Message | None, image_path: str, division: med.DivisionMetadata) -> str:
        with try_nest(msg, f"Adding division emblem from image at {image_path}") as _:
            return add_image(self.ndf[ndf_paths.DIVISION_TEXTURES],
                             image_path,
                             self.metadata.folder_path,
                             "Assets/2D/Interface/UseOutGame/Division/Emblem",
                             division.emblem_namespace, 
                             "DivisionAdditionalTextureBank")
        
    def try_add_button_texture(self: Self, image_path: str | None, unit: meu.UnitMetadata) -> str | None:
        if image_path is None:
            return None
        return self.add_button_texture(None, image_path, unit)
    
    def add_button_texture(self: Self, msg: Message | None, image_path: str, unit: meu.UnitMetadata) -> str:
        with try_nest(msg, f'Adding button texture from image at {image_path}') as _:
            return add_image_literal(self.ndf[ndf_paths.BUTTON_TEXTURES_UNITES],
                                     image_path,
                                     self.metadata.folder_path,
                                     'Assets/2D/Interface/Common/UnitsIcons',
                                     unit.button_texture_name,
                                     'UnitButtonTextureAdditionalBank')
        
    def write_edits(self: Self, msg: Message | None = None) -> None:
        if msg is None:
            msg = self.root_msg
        for edit in self.mod.edits:
            with msg.nest(f"Writing {edit.file_path}") as _:
                self.mod.write_edit(edit)
        
    def generate_and_write_localization(self: Self, msg: Message | None = None) -> None:
        if msg is None:
            msg = self.root_msg
        csv = self.localization.generate_csv(msg)
        with msg.nest("Writing localization") as msg:
            with open(self.metadata.localization_path, "w") as file:
                file.write(csv)

    def create_ammo(self: Self, name: str, copy_of: str) -> ca.AmmoCreator:
        return ca.AmmoCreator(self.ndf, ensure.prefix(name, f'Ammo_{self.prefix}_'), copy_of, self.guids)
    
    def get_unit_object(self: Self, unit: str, showroom: bool = False) -> Object:
        path = ndf_paths.UNITE_DESCRIPTOR if not showroom else ndf_paths.SHOWROOM_UNITS
        return self.ndf[path].by_name(ensure.unit_descriptor(unit, showroom)).value
    
    def get_unit(self: Self, unit: str | Object, showroom: bool = False) -> wu.UnitWrapper:
        if not isinstance(unit, Object):
            unit = self.get_unit_object(unit, showroom)
        return wu.UnitWrapper(self, unit)