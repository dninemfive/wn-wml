
from metadata.division import DivisionMetadata
from metadata.mod import ModMetadata
from message import Message, try_nest
from metadata.division_unit_registry import DivisionUnitRegistry
from misc.cache_set import CacheSet
from misc.division_creator import DivisionCreator
from ndf_parse import Mod
from ndf_parse.model import List
from ndf_parse.model.abc import CellValue
from ndf_paths import DIVISION_TEXTURES
from paths import CACHE_FOLDER
from typing import Self
from utils.ndf import add_image
from uuid import uuid4
# https://stackoverflow.com/a/2823331
import random
import string

GUID = "guid"
LOCALIZATION = "localization"
UNIT_ID = "unit_id"
CHARACTERS = [*string.ascii_letters, *[str(x) for x in range(10)]]

class ModCreationContext(object):
    @property
    def prefix(self: Self) -> str:
        return self.metadata.dev_short_name

    @property
    def msg_length(self: Self):
        return max([len(x) for x in self.paths]) + len("Editing ")
    
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

    def generate_guid(self: Self, guid_key: str) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result
    
    def register(self: Self, string: str) -> str:
        """ Registers a localized string in the localization cache. Returns the __key__ generated for this string! """
        if string in self.localization_cache:
            return f"'{self.localization_cache[string]}'"
        if len(self.metadata.localization_prefix) > 5:
            raise Exception("Localization prefix cannot be longer than 5 characters, as keys must be 10 or fewer characters total!")
        key = self.generate_key()
        while key in self.localization_cache.values():
            key = self.generate_key()
        # intentionally backward: we want to be able to look up strings by their values
        self.localization_cache[string] = key
        return f"'{key}'"

    def generate_key(self: Self) -> str:
        result = self.metadata.localization_prefix
        for _ in range(10 - len(result)):
            result += random.choice(CHARACTERS)
        return result

    def generate_localization_csv(self: Self, msg: Message | None) -> str:
        if msg is None:
            msg = self.root_msg
        result = '"TOKEN";"REFTEXT"'
        with msg.nest("Generating localization") as msg2:
            for k in sorted(self.localization_cache.keys()):
                with msg2.nest(f"{self.localization_cache[k]}\t{k}") as _:
                    result += "\n" + f'"{self.localization_cache[k]}";"{k}"'
        return result
    
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
        csv = self.generate_localization_csv(msg)
        with msg.nest("Writing localization") as msg:
            with open(self.metadata.localization_path, "w") as file:
                file.write(csv)