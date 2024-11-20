from typing import Iterable

from ._constants._file_targets import TARGET_SETS
from ._constants._resolvers import _enum_resolver, _format_resolver
from ._types._member_def import MemberDef


def _init_lines() -> Iterable[str]:
    yield f'# File automatically generated by {__file__.split('src\\')[1]}'
    yield 'from typing import Literal'
    yield 'from .paths import *'
    for target_set in TARGET_SETS:
        yield f'# Automatically generated from {target_set.file_path}'
        yield from target_set.to_lines(MemberDef.literal_lines)

def _validation_lines() -> Iterable[str]:
    yield f'# File automatically generated by {__file__.split('src\\')[1]}'
    yield f'from warno_mfw.hints._generate._constants._resolvers import {_enum_resolver.__name__}, {_format_resolver.__name__}'
    for target_set in TARGET_SETS:
        yield f'# Automatically generated from {target_set.file_path}'
        yield from target_set.to_lines(MemberDef.resolver_lines)