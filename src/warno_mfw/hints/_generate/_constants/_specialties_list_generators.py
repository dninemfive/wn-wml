from typing import Iterable

from warno_mfw.utils.ndf import ensure

from .._types._member_def import MemberDef
from ._base_code_generators import (MEMBER_LEN, _base_literal_generator,
                                    _enum_resolver_generator)

_PRIMARY_SPECIALTY, _SECONDARY_SPECIALTY = 'PrimarySpecialty', 'SecondarySpecialty'

def _split_values(member_def: MemberDef) -> tuple[dict[str, str], dict[str, str]]:
    primaries, secondaries = {}, {}
    for k, v in member_def.values.items():
        (secondaries if k.startswith('_') else primaries)[ensure.no_prefix(k, '_')] = v
    return (primaries, secondaries)


def _specialties_list_literal_generator(member_def: MemberDef) -> Iterable[str]:
    primaries, secondaries = _split_values(member_def)
    yield _base_literal_generator(_PRIMARY_SPECIALTY,   primaries.keys())
    yield _base_literal_generator(_SECONDARY_SPECIALTY, secondaries.keys())
    yield f'{f'AnySpecialty'.ljust(MEMBER_LEN)}= {_PRIMARY_SPECIALTY} | {_SECONDARY_SPECIALTY}'

def _specialties_list_resolver_generator(member_def: MemberDef) -> Iterable[str]:
    primaries, secondaries = _split_values(member_def)
    yield _enum_resolver_generator(_PRIMARY_SPECIALTY, None, primaries)
    yield _enum_resolver_generator(_SECONDARY_SPECIALTY, None, secondaries)