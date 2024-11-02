from dataclasses import dataclass
from typing import Self

import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.metadata.unit import UnitMetadata


@dataclass
class _SquadKeys(object):
    metadata: UnitMetadata

    @property
    def _all_weapon_alternatives(self: Self) -> str:
        return ensure.prefix(self.metadata.name, 'AllWeaponAlternatives_')

    @property
    def _all_weapon_sub_depiction(self: Self) -> str:
        return ensure.prefix(self.metadata.name, 'AllWeaponSubDepiction_')

    @property
    def _all_weapon_sub_depiction_backpack(self: Self) -> str:
        return ensure.prefix(self.metadata.name, 'AllWeaponSubDepictionBackpack_')
    
    @property
    def _unit(self: Self) -> str:
        return self.metadata.quoted_name

    @property
    def _tactic_depiction_alternatives(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Alternatives'

    @property
    def _tactic_depiction_soldier(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Soldier'
    
    @property
    def _tactic_depiction_ghost(self: Self) -> str:
        return f'TacticDepiction_{self.metadata.name}_Ghost'