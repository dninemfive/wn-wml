from typing import Iterable, Self

import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.wrappers.str_list import StrListWrapper
from ndf_parse.model import List, Object

from ._abc import UnitModuleKey, UnitModuleWrapper, get_t_module_selector

_SKILL_PREFIX = '$/GFX/EffectCapacity/Capacite_'
_SELECTION_PREFIX = '~/'

class CapaciteModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TCapaciteModuleDescriptor')
    _get_method = get_t_module_selector

    def __contains__(self: Self, skill: str) -> bool:
        return skill in self.DefaultSkillList
    
    def __iter__(self: Self) -> Iterable[str]:
        yield from self.DefaultSkillList

    @property
    def _default(self: Self) -> Object:
        return self.object.by_member('Default').value

    @property
    def _default_skill_list(self: Self) -> List:
        return self._default.by_member('DefaultSkillList').value

    @property
    def DefaultSkillList(self: Self) -> StrListWrapper:
        if not hasattr(self, '_default_skill_list_wrapper'):
            self._default_skill_list_wrapper = StrListWrapper(self._default_skill_list,
                                                              (lambda x: ensure.prefix(x,    _SKILL_PREFIX),
                                                               lambda x: ensure.no_prefix(x, _SKILL_PREFIX)))
        return self._default_skill_list_wrapper  
    
    @DefaultSkillList.setter
    def DefaultSkillList(self: Self, value: list[str] | List) -> None:
        if hasattr(self, '_default_skill_list_wrapper'):
            delattr(self, '_default_skill_list_wrapper')
        edit.member(self._default, 'DefaultSkillList', ensure.all(value, lambda x: ensure.prefix(x, _SKILL_PREFIX)))

    @property
    def Selection(self: Self) -> StrListWrapper:
        if not hasattr(self, '_selection'):
            self._selection = StrListWrapper(self.object.by_member('Selection').value,
                                             (lambda x: ensure.prefix(x,    _SELECTION_PREFIX),
                                              lambda x: ensure.no_prefix(x, _SELECTION_PREFIX)))
        return self._selection
    
    @Selection.setter
    def Selection(self: Self, value: list[str] | List) -> None:
        if hasattr(self, '_selection'):
            delattr(self, '_selection')
        edit.member(self.object, 'Selection', ensure.all(value, lambda x: ensure.prefix(x, _SELECTION_PREFIX)))