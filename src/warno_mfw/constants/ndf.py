from typing import Iterable
from .literals import MotherCountry, Nationalite

DISPERSION_COLOR     = 'RGBA[0,0,0,0]'
DISPERSION_THICKNESS = -0.1

COUNTRY_CODE_TO_COUNTRY_SOUND_CODE: dict[str, str] = {
    'DDR':  'GER',
    'RFA':  'GER',
    'SOV':  'SOVIET',
    'UK' :  'UK',
    'US' :  'US',
    'POL':  'SOVIET'
}
def many_to_one(**keys: Iterable[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for v, ks in keys.items():
        for k in ks:
            result[k] = v
    return result

COUNTRY_CODE_TO_NATIONALITE: dict[MotherCountry, Nationalite] = many_to_one(
    Allied  =   ['BEL', 'FR',  'RFA', 'UK',  'US'],
    Axis    =   ['DDR', 'POL', 'SOV', 'TCH']
)