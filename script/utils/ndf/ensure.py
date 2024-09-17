from ndf_parse.model import ListRow, MapRow, MemberRow
from ndf_parse.model.abc import CellValue

def listrow(val: CellValue | ListRow) -> ListRow:
    if isinstance(val, ListRow):
        return val
    else:
        return ListRow(value=val)
    
def maprow(pair_or_key: tuple[str, CellValue] | MapRow | str, value_or_none: CellValue | None = None):
    if isinstance(pair_or_key, str):
        if value_or_none is None:
            raise ValueError("If first argument is not a tuple or MapRow, second argument must not be None!")
        return MapRow(k=pair_or_key, v=value_or_none)
    elif isinstance(pair_or_key, MapRow):
        return pair_or_key
    else:
        return MapRow(k=pair_or_key[0], v=pair_or_key[1])
    
def memberrow(pair_or_key: tuple[str, CellValue] | MemberRow | str, value_or_none: CellValue | None = None):
    if isinstance(pair_or_key, str):
        if value_or_none is None:
            raise ValueError("If first argument is not a tuple or MemberRow, second argument must not be None!")
        return MemberRow(k=pair_or_key, v=value_or_none)
    elif isinstance(pair_or_key, MemberRow):
        return pair_or_key
    else:
        return MemberRow(k=pair_or_key[0], v=pair_or_key[1])

def unit_path(descriptor: str) -> str:
    return descriptor if descriptor.startswith("$/GFX/Unit/") else f'$/GFX/Unit/{descriptor}'

def quotes(s: str, quote: str = '"') -> str:
    if not s.startswith(quote):
        s = f'{quote}{s}'
    if not s.endswith(quote):
        s = f'{s}{quote}'
    return s