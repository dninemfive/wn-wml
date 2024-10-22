from __future__ import annotations

from typing import Any, Callable, Iterable, Self, Type

from wrappers._abc import NdfObjectWrapper
from wrappers.list import ListWrapper
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
from constants.primitive_types import MotherCountry
# from context.mod_creation import ModCreationContext
from ndf_parse.model import Object
import wrappers._modules


class WeaponManagerWrapper(NdfObjectWrapper):
    # ctx: ModCreationContext
    def __init__(self: Self, ctx, object: Object):
        self.ctx = ctx
        self.object = object
        self._salves: ListWrapper[int] = ListWrapper(self.object.by_member('Salves').value)
        self._salvo_is_main_salvo: ListWrapper[bool] = ListWrapper(self.object.by_member('SalvoIsMainSalvo').value)

    @property
    def Salves(self: Self) -> Iterable[int]:
        yield from self._salves
    
    @Salves.setter
    def Salves(self: Self, value: list[int]) -> None:
        edit.member(self.object, 'Salves', value)
        self._salves = ListWrapper(self.object.by_member('Salves').value)

    @property
    def AlwaysOrientArmorTowardsThreat(self: Self) -> bool:
        return bool(self._get('AlwaysOrientArmorTowardsThreat'))
    
    @AlwaysOrientArmorTowardsThreat.setter
    def AlwaysOrientArmorTowardsThreat(self: Self, value: bool) -> None:
        self._set('AlwaysOrientArmorTowardsThreat', value)

    