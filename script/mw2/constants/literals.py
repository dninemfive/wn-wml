from typing import Literal

AcknowUnitType                          = Literal['AirSup',
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
                                                  'Vehicle']

MotherCountry                           = Literal['BEL',
                                                  'DDR',
                                                  'FR',
                                                  'POL',
                                                  'RFA',
                                                  'SOV',
                                                  'TCH',
                                                  'UK',
                                                  'US']

Nationalite                             = Literal['Allied',
                                                  'Axis']

TypeUnitFormation                       = Literal['Artillerie',
                                                  'Char',
                                                  'None',
                                                  'Reconnaissance',
                                                  'Supply']

Factory                                 = Literal['Art',
                                                  'DCA',
                                                  'Helis',
                                                  'Infantry',
                                                  'Logistic',
                                                  'Planes',
                                                  'Recons',
                                                  'Tanks']

InfoPanelConfigurationToken             = Literal['Default',
                                                  'HelicoDefault',
                                                  'HelicoSupplier',
                                                  'HelicoTransporter',
                                                  'Infantry',
                                                  'VehiculeSupplier',
                                                  'VehiculeTransporter',
                                                  'avion']

TypeStrategicCount                      = Literal['AA',
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
                                                  'Transport']

UnitRole                                = Literal['tank_A',
                                                  'tank_B',
                                                  'tank_C',
                                                  'tank_D']

MenuIconTexture                         = Literal['AA',
                                                  'AA_air',
                                                  'AA_hel',
                                                  'AA_veh',
                                                  'AT',
                                                  'ATGM_air',
                                                  'ATGM_hel',
                                                  'ATGun',
                                                  'AT_veh',
                                                  'Armor',
                                                  'Armor_heavy',
                                                  'CMD_hel',
                                                  'CMD_inf',
                                                  'CMD_tank',
                                                  'CMD_veh',
                                                  'HMG',
                                                  'Infantry',
                                                  'RECO_hel',
                                                  'RECO_inf',
                                                  'RECO_veh',
                                                  'SEAD_air',
                                                  'Support_air',
                                                  'Support_hel',
                                                  'appui',
                                                  'assault',
                                                  'hel',
                                                  'hel_supply',
                                                  'howitzer',
                                                  'ifv',
                                                  'manpad',
                                                  'mlrs',
                                                  'mortar',
                                                  'reco',
                                                  'supply',
                                                  'transport_noweapon',
                                                  'transport_small']