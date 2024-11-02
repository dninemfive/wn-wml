from dataclasses import dataclass
from typing import Self

import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.metadata.unit import UnitMetadata


@dataclass
class _TowedKeys(object):
    metadata: UnitMetadata

    @property
    def _depiction_path(self: Self) -> str:
        return ensure.prefix_and_suffix(self.metadata.name, '~/Gfx_', '_Autogen')