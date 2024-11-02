from typing import Literal, LiteralString, Self, Type

import utils.ndf.ensure as ensure

from .ndf import (COUNTRY_CODE_TO_COUNTRY_SOUND_CODE,
                  COUNTRY_CODE_TO_NATIONALITE)


# TODO: generate these from source
class NdfEnum(object):
    def __init__(self: Self, prefix: str, suffix: str, *values: str):
        self.prefix = prefix
        self.suffix = suffix
        self.values = values

    def ensure_valid(self: Self, s: str) -> str:
        s = ensure.prefix_and_suffix(s, self.prefix, self.suffix)
        assert s in self.values, f'{s} is not one of the valid values: {str(self.values)}'
        return s
    
    # TODO: way to alias enums (e.g. Factory: REC = 'Recons')

# not staticmethod because that doesn't preserve type hints???
def NdfEnum_literals(*values: str) -> NdfEnum:
    return NdfEnum("'", "'", *[ensure.quoted(x, "'") for x in values])

def NdfEnum_with_path(path: str, *values: str) -> NdfEnum:
    return NdfEnum(path, '', *[ensure.prefix(x, path) for x in values])

WeaponType: NdfEnum                     = NdfEnum_literals('bazooka',
                                                           'grenade',
                                                           'mmg',
                                                           'smg')
CountrySoundCode: NdfEnum               = NdfEnum_literals('GER',
                                                           'SOVIET',
                                                           'UK',
                                                           'US')
AcknowUnitType                          = NdfEnum_with_path('~/TAcknowUnitType_',
                                                            'AirSup',
                                                            'Air_CAS',
                                                            'ArtShell',
                                                            'CanonAA',
                                                            'Command',
                                                            'CommandVehicle',
                                                            'Command_Infantry',
                                                            'Engineer',
                                                            'GroundAtk',
                                                            'GunArtillery',
                                                            'HeliAttack',
                                                            'HeliTransport',
                                                            'Inf',
                                                            'Inf2',
                                                            'Inf_Elite',
                                                            'Inf_Militia',
                                                            'KaJaPa',
                                                            'Logistic',
                                                            'MLRS',
                                                            'Multirole',
                                                            'Reco',
                                                            'Recon_INF',
                                                            'Recon_Vehicle',
                                                            'SAM',
                                                            'Tank',
                                                            'TankDestroyer',
                                                            'TankDestroyerMissile',
                                                            'Transport',
                                                            'Vehicle')

# TODO: automate defining custom countries
#   needs sound code, flag, name, idk what else
MotherCountry                           =  NdfEnum_literals('BEL',
                                                            'DDR',
                                                            'FR',
                                                            'POL',
                                                            'RFA',
                                                            'SOV',
                                                            'TCH',
                                                            'UK',
                                                            'US')

Nationalite                             = NdfEnum_with_path('ENationalite/',
                                                            'Allied',
                                                            'Axis')

TypeUnitFormation                       =  NdfEnum_literals('Artillerie',
                                                            'Char',
                                                            'None',
                                                            'Reconnaissance',
                                                            'Supply')

Factory                                 = NdfEnum_with_path('EDefaultFactories/',
                                                            'Art',
                                                            'DCA',
                                                            'Helis',
                                                            'Infantry',
                                                            'Logistic',
                                                            'Planes',
                                                            'Recons',
                                                            'Tanks')

InfoPanelConfigurationToken             =  NdfEnum_literals('Default',
                                                            'HelicoDefault',
                                                            'HelicoSupplier',
                                                            'HelicoTransporter',
                                                            'Infantry',
                                                            'VehiculeSupplier',
                                                            'VehiculeTransporter',
                                                            'avion')

TypeStrategicCount                      = NdfEnum_with_path('ETypeStrategicDetailedCount/',
                                                            'AA',
                                                            'AA_Hel',
                                                            'AA_Veh',
                                                            'AT',
                                                            'AT_Gun',
                                                            'AT_Hel',
                                                            'AT_Veh',
                                                            'Air_AA',
                                                            'Air_AT',
                                                            'Air_Sead',
                                                            'Air_Support',
                                                            'Armor',
                                                            'Armor_Heavy',
                                                            'CMD_Hel',
                                                            'CMD_Inf',
                                                            'CMD_Tank',
                                                            'CMD_Veh',
                                                            'Engineer',
                                                            'Hel_Support',
                                                            'Hel_Transport',
                                                            'Howitzer',
                                                            'Ifv',
                                                            'Infantry',
                                                            'Manpad',
                                                            'Mlrs',
                                                            'Mortar',
                                                            'Reco',
                                                            'Reco_Hel',
                                                            'Reco_Inf',
                                                            'Reco_Veh',
                                                            'Supply',
                                                            'Supply_Hel',
                                                            'Support',
                                                            'Transport')

UnitRole                                =  NdfEnum_literals('tank_A',
                                                            'tank_B',
                                                            'tank_C',
                                                            'tank_D')

def country_sound_code(country: str) -> str:
    country = MotherCountry.ensure_valid(country)
    if country in COUNTRY_CODE_TO_COUNTRY_SOUND_CODE:
        return COUNTRY_CODE_TO_COUNTRY_SOUND_CODE[country]
    return country

def nationalite(country: str) -> str:
    assert country in COUNTRY_CODE_TO_NATIONALITE, 'Can currently only look up preexisting countries in the nationalite table!'
    return COUNTRY_CODE_TO_NATIONALITE[country]