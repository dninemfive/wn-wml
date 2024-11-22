from typing import Self

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

    @property
    def DefaultSkillList(self: Self) -> StrListWrapper:
        if not hasattr(self, '_default_skill_list'):
            self._default_skill_list = StrListWrapper(self.object.by_member('Default').value.by_member('DefaultSkillList').value,
                                             (lambda x: ensure.prefix(x,    _SKILL_PREFIX),
                                              lambda x: ensure.no_prefix(x, _SKILL_PREFIX)))
        return self._default_skill_list

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