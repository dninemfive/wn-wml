from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
import utils.ndf.ensure as ensure

def dict_to_Map(input: dict[str, CellValue]) -> Map:
    result = Map()
    for k, v in input.items():
        result.add(MapRow((k, str(v))))
    return result

def list(*items: CellValue | ListRow) -> List:
    result = List()
    for item in items:
        result.add(ensure.listrow(item))
    return result

def map(**items: tuple[str, CellValue] | MapRow) -> Map:
    result = Map()
    for k, v in items.items():
        result.add(ensure.maprow((k, v)))

def object(type: str, **props: CellValue) -> Object:
    result = Object(type)
    for k, v in props.items():
        result.add(MemberRow(value=v, member=k))
    return result