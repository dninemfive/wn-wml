from typing import Self

from constants.misc import GUID, LOCALIZATION, MESSAGE_PADDING, UNIT_ID
from constants.ndf_paths import BUTTON_TEXTURES_UNITES, DIVISION_TEXTURES
from constants.paths import CACHE_FOLDER
from creators.division import DivisionCreator
from creators.unit import UnitCreator
from managers.guid import GuidManager
from managers.localization import LocalizationManager
from managers.unit_id import UnitIdManager
from metadata.division import DivisionMetadata
from metadata.division_unit_registry import DivisionUnitRegistry
from metadata.mod import ModMetadata
from metadata.new_unit import NewUnitMetadata
from metadata.unit import UnitMetadata
from ndf_parse import Mod
from ndf_parse.model import List
from ndf_parse.model.abc import CellValue
from utils.ndf.files import add_image, add_image_literal
from utils.types.cache_set import CacheSet
from utils.types.message import Message, try_nest


class ModCreationContext(object):
    @property
    def prefix(self: Self) -> str:
        return self.metadata.dev_short_name
    
    @property
    def guid_cache(self: Self) -> dict[str, str]:
        return self.caches[GUID]
    
    @property
    def localization_cache(self: Self) -> dict[str, str]:
        return self.caches[LOCALIZATION]
    
    @property
    def unit_id_cache(self: Self) -> dict[str, str]:
        return self.caches[UNIT_ID]
    
    def __init__(self: Self, metadata: ModMetadata, root_msg: Message | None, *ndf_paths: str):
        self.metadata = metadata
        self.mod = Mod(metadata.folder_path, metadata.folder_path)
        self.root_msg = root_msg
        self.paths = ndf_paths
        self.caches = CacheSet(CACHE_FOLDER, GUID, LOCALIZATION, UNIT_ID)
        self.guids = GuidManager(self.guid_cache)
        self.localization = LocalizationManager(self.localization_cache, self.metadata.localization_prefix)
       
    def __enter__(self: Self) -> Self:
        self.mod.check_if_src_is_newer()
        with try_nest(self.root_msg, "Loading ndf files", child_padding=MESSAGE_PADDING) as msg:
            self.ndf = {x:self.load_ndf(x, msg) for x in self.paths}
        self.caches.load(self.root_msg)
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        with self.root_msg.nest("Saving mod", child_padding=MESSAGE_PADDING) as write_msg:
            self.write_edits(write_msg)
            self.generate_and_write_localization(write_msg)
        self.caches.save(self.root_msg)
    
    def load_ndf(self: Self, path: str, msg: Message) -> List:
        with msg.nest(f"Loading {path}") as _:
            return self.mod.edit(path).current_tree
    
    def create_division(self: Self,
                        division: DivisionMetadata,
                        copy_of: str,
                        units: DivisionUnitRegistry,
                        insert_after: str | None = None,
                        root_msg: Message | None = None,
                        **changes: CellValue | None) -> None:
        with try_nest(root_msg, 
                      f"Making division {division.short_name}",
                      child_padding=MESSAGE_PADDING) as msg:
            DivisionCreator(self.guids.generate(division.descriptor_name), copy_of, insert_after, division, units, **changes).apply(self.ndf, msg)

    def start_unit_ids_at(self: Self, initial_id: int) -> UnitIdManager:
        return UnitIdManager(self.unit_id_cache, initial_id)
    
    def create_unit(self: Self, name: str, country: str, copy_of: str, showroom_src: str | None = None, button_texture_src_path: str | None = None) -> UnitCreator:
        # TODO: msg here
        metadata: NewUnitMetadata = NewUnitMetadata.from_(self.prefix, name, country, self.guids, self.localization)
        return UnitCreator(self.ndf,
                           metadata,
                           copy_of,
                           showroom_src,
                           self.try_add_button_texture(button_texture_src_path, metadata.unit_metadata),
                           self.root_msg)
    
    def add_division_emblem(self: Self, msg: Message | None, image_path: str, division: DivisionMetadata) -> str:
        with try_nest(msg, f"Adding division emblem from image at {image_path}") as _:
            return add_image(self.ndf[DIVISION_TEXTURES],
                             image_path,
                             self.metadata.folder_path,
                             "Assets/2D/Interface/UseOutGame/Division/Emblem",
                             division.emblem_namespace, 
                             "DivisionAdditionalTextureBank")
        
    def try_add_button_texture(self: Self, image_path: str | None, unit: UnitMetadata) -> str | None:
        if image_path is None:
            return None
        return self.add_button_texture(None, image_path, unit)
    
    def add_button_texture(self: Self, msg: Message | None, image_path: str, unit: UnitMetadata) -> str:
        with try_nest(msg, f'Adding button texture from image at {image_path}') as _:
            return add_image_literal(self.ndf[BUTTON_TEXTURES_UNITES],
                                     image_path,
                                     self.metadata.folder_path,
                                     'Assets/2D/Interface/Common/UnitsIcons',
                                     unit.button_texture_key,
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