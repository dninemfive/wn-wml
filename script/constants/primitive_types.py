from typing import Literal, Self

import utils.ndf.ensure as ensure

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

    def literals(self: Self, *values: str) -> Self:
        return NdfEnum("'", "'", [ensure.quoted(x, "'") for x in values])
    
    def with_path(self: Self, path: str, *values: str) -> Self:
        return NdfEnum(path, '', [ensure.prefix(x, path) for x in values])

WeaponType: NdfEnum = NdfEnum.literals('bazooka', 'grenade', 'mmg', 'smg')
CountrySoundCode: NdfEnum = NdfEnum.literals('GER', 'SOVIET', 'UK', 'US')

AcknowUnitType                          = NdfEnum.with_path('~/TAcknowUnitType_',
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
MotherCountry                           =  NdfEnum.literals('BEL',
                                                            'DDR',
                                                            'FR',
                                                            'POL',
                                                            'RFA',
                                                            'SOV',
                                                            'TCH',
                                                            'UK',
                                                            'US')

Nationalite                             = NdfEnum.with_path('ENationalite/',
                                                            'Allied',
                                                            'Axis')

TypeUnitFormation                       =  NdfEnum.literals('Artillerie',
                                                            'Char',
                                                            'None',
                                                            'Reconnaissance',
                                                            'Supply')

Factory                                 = NdfEnum.with_path('EDefaultFactories/',
                                                            'Art',
                                                            'DCA',
                                                            'Helis',
                                                            'Infantry',
                                                            'Logistic',
                                                            'Planes',
                                                            'Recons',
                                                            'Tanks')

InfoPanelConfigurationToken             =  NdfEnum.literals('Default',
                                                            'HelicoDefault',
                                                            'HelicoSupplier',
                                                            'HelicoTransporter',
                                                            'Infantry',
                                                            'VehiculeSupplier',
                                                            'VehiculeTransporter',
                                                            'avion')

TypeStrategicCount                      = NdfEnum.with_path('ETypeStrategicDetailedCount/',
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

UnitRole                                =  NdfEnum.literals('tank_A',
                                                            'tank_B',
                                                            'tank_C',
                                                            'tank_D')