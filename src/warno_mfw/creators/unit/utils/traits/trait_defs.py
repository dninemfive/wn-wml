from .trait_def import TraitDef
from .trait_operation import CapaciteOperation as Capacite

SHOCK               = TraitDef('choc',
                               Capacite('Choc'))
ELECTRONIC_WARFARE  = TraitDef('electronic_warfare',
                               Capacite('electronic_warfare'))
# TODO: i believe this also separately modifies the ECM property. would need to change traitdefs to include a series of edits.
DAZZLER             = TraitDef('eo_dazzler',
                               Capacite('eo_dazzler'))
FIRE_DIRECTION      = TraitDef('fireDirection',
                               Capacite('fireDirection'))
GSR                 = TraitDef('gsr',
                               Capacite('GSR',
                                        'GSR_no_GSR'))
JAMMER              = TraitDef('jammer',
                               Capacite('jammer',
                                        'jammer_arty'))
MP                  = TraitDef('mp',
                               Capacite('MilitaryPolice'))
RESERVIST           = TraitDef('reservist',
                               Capacite('reserviste'))
RESOLUTE            = TraitDef('resolute',
                               Capacite('resolute'))
SECURITY            = TraitDef('security',
                               Capacite('security'))
SIGINT              = TraitDef('singint',
                               Capacite('sigint_close',
                                        'sigint_far'))
SNIPER              = TraitDef('sniper',
                               Capacite('sniper', 'sniper_no_snipe'))