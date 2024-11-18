from typing import Iterable

from warno_mfw.utils.ndf import ensure

from .._types._member_def import MemberDef
from ._base_formatter import _base_formatter

def _specialties_list_formatter(member_def: MemberDef) -> Iterable[str]:
    primaries, secondaries = [], []
    for item in member_def.values:
        (secondaries if item.startswith('_') else primaries).append(item)
    yield _base_formatter('PrimarySpecialty',   primaries)
    yield _base_formatter('SecondarySpecialty', [ensure.no_prefix(x, '_') for x in secondaries])