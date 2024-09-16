from creators.division_creator import DivisionCreator
from creators.unit_creator import UnitCreator
from managers.guid_manager import GuidManager
from managers.localization_manager import LocalizationManager
from managers.unit_id_manager import UnitIdManager
from metadata.division import DivisionMetadata
from metadata.mod import ModMetadata
from metadata.division_unit_registry import DivisionUnitRegistry
from ndf_parse import Mod
from ndf_parse.model import List
from ndf_parse.model.abc import CellValue
from globals.ndf_paths import DIVISION_TEXTURES
from globals.paths import CACHE_FOLDER
from globals.misc import GUID, LOCALIZATION, UNIT_ID
from typing import Self
from utils.ndf import add_image
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
        self.unit_ids = UnitIdManager(self, 139000)
       
    def __enter__(self: Self) -> Self:
        self.mod.check_if_src_is_newer()
        with try_nest(self.root_msg, "Loading ndf files", child_padding=self.msg_length) as msg:
            self.ndf = {x:self.load_ndf(x, msg) for x in self.paths}
        self.caches.load(self.root_msg)
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        with self.root_msg.nest("Saving mod", child_padding=self.msg_length) as write_msg:
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
                      child_padding=self.msg_length) as msg:
            DivisionCreator(self.generate_guid(division.descriptor_name), copy_of, insert_after, division, units, **changes).apply(self.ndf, msg)
    
    def create_unit(self: Self, name: str, country: str, copy_of: str) -> UnitCreator:
        return UnitCreator(self, self.prefix, name, country, copy_of)
    
    def add_division_emblem(self: Self, msg: Message | None, image_path: str, division: DivisionMetadata) -> str:
        with try_nest(msg, f"Adding division emblem from image at {image_path}") as _:
            return add_image(self.ndf[DIVISION_TEXTURES],
                             image_path,
                             self.metadata.folder_path,
                             "Assets/2D/Interface/UseOutGame/Division/Emblem",
                             division.emblem_namespace, 
                             "DivisionAdditionalTextureBank")
        
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