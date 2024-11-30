from typing import Iterable
from warno_mfw import hints
from warno_mfw.hints._validation import _resolve_MotherCountry

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

COUNTRY_CODE_TO_NATIONALITE: dict[hints.MotherCountry, hints.Coalition] = many_to_one(
    Allied  =   ['BEL', 'FR',  'RFA', 'UK',  'US'],
    Axis    =   ['DDR', 'POL', 'SOV', 'TCH']
)

def country_sound_code(country: str) -> str:
    country = _resolve_MotherCountry(country)
    if country in COUNTRY_CODE_TO_COUNTRY_SOUND_CODE:
        return COUNTRY_CODE_TO_COUNTRY_SOUND_CODE[country]
    return country

def coalition(country: str) -> str:
    assert country in COUNTRY_CODE_TO_NATIONALITE, 'Can currently only look up preexisting countries in the coalition table!'
    return COUNTRY_CODE_TO_NATIONALITE[country]