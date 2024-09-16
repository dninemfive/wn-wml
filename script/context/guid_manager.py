from context.mod_creation_context import ModCreationContext
from message import Message
from misc.unit_creator import UnitCreator
from ndf_parse.model import List
from typing import Self
from uuid import uuid4

class GuidManager(object):
    def __init__(self: Self, cache: dict[str, str]):
        self.__cache = cache
    
    def generate_guid(self: Self, guid_key: str) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.__cache:
            return self.__cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.__cache[guid_key] = result
        return result