from typing import Literal, LiteralString, Self, Type

import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.hints._validation import _resolve_MotherCountry

from .ndf import (COUNTRY_CODE_TO_COUNTRY_SOUND_CODE,
                  COUNTRY_CODE_TO_NATIONALITE)

def country_sound_code(country: str) -> str:
    country = _resolve_MotherCountry(country)
    if country in COUNTRY_CODE_TO_COUNTRY_SOUND_CODE:
        return COUNTRY_CODE_TO_COUNTRY_SOUND_CODE[country]
    return country

def nationalite(country: str) -> str:
    assert country in COUNTRY_CODE_TO_NATIONALITE, 'Can currently only look up preexisting countries in the nationalite table!'
    return COUNTRY_CODE_TO_NATIONALITE[country]