from .trait_def import TraitDef
from .trait_operation import CapaciteOperation as Capacite, FalseFlagOperation

TODO = None

AMPHIBIOUS          = TraitDef('amphibie',
                               TODO)
CAN_BE_AIRLIFTED    = TraitDef('canBeAirlifted',
                               TODO)
SHOCK               = TraitDef('choc',
                               Capacite('Choc'))
ELECTRONIC_WARFARE  = TraitDef('electronic_warfare',
                               Capacite('electronic_warfare'))
ERA                 = TraitDef('era',
                               TODO)
DAZZLER             = TraitDef('eo_dazzler',
                               Capacite('eo_dazzler'))
FALSE_FLAG          = TraitDef('falseflag',
                               FalseFlagOperation())
FIRE_DIRECTION      = TraitDef('fireDirection',
                               Capacite('fireDirection'))
GSR                 = TraitDef('gsr',
                               Capacite('GSR',
                                        'GSR_no_GSR'))
# i believe this one has a different effect on infantry vs transport units
IFV                 = TraitDef('ifv',
                               TODO)
JAMMER              = TraitDef('jammer',
                               Capacite('jammer',
                                        'jammer_arty'))
LEADER              = TraitDef('leader',
                               TODO)
MILITARY_POLICE     = TraitDef('mp',
                               Capacite('MilitaryPolice'))
AIRBORNE            = TraitDef('para',
                               TODO)
RESERVIST           = TraitDef('reservist',
                               Capacite('reserviste'))
RESOLUTE            = TraitDef('resolute',
                               Capacite('resolute'))
SECURITY            = TraitDef('security',
                               Capacite('security'))
SPECIAL_FORCES      = TraitDef('sf',
                               TODO)
SMOKE_LAUNCHER      = TraitDef('smoke_launcher',
                               TODO)
SIGINT              = TraitDef('singint',
                               Capacite('sigint_close',
                                        'sigint_far'))
SNIPER              = TraitDef('sniper',
                               Capacite('sniper', 'sniper_no_snipe'))
TRANSPORT           = TraitDef('transport1',
                               TODO)
PRIME_MOVER         = TraitDef('transport2',
                               TODO)