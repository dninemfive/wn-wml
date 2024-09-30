from dataclasses import dataclass
from typing import Self

import utils.ndf.ensure as ensure
from metadata.unit import UnitMetadata


@dataclass
class _TowedKeys(object):
    metadata: UnitMetadata

    @property
    def _depiction_path(self: Self) -> str:
        return ensure.prefix_and_suffix(self.metadata.name, '~/Gfx_', '_Autogen')