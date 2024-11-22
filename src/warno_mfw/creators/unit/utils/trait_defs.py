from warno_mfw.creators.unit.utils.trait_def import CapaciteTraitDef

SHOCK               = CapaciteTraitDef('choc',                  'Choc')
ELECTRONIC_WARFARE  = CapaciteTraitDef('electronic_warfare',    'electronic_warfare')
# TODO: i believe this also separately modifies the ECM property. would need to change traitdefs to include a series of edits.
DAZZLER             = CapaciteTraitDef('eo_dazzler',            'eo_dazzler')
FIRE_DIRECTION      = CapaciteTraitDef('fireDirection',         'fireDirection')
GSR                 = CapaciteTraitDef('gsr',                   'GSR',                  'GSR_no_GSR')
JAMMER              = CapaciteTraitDef('jammer',                'jammer',               'jammer_arty')
MP                  = CapaciteTraitDef('mp',                    'MilitaryPolice')
RESERVIST           = CapaciteTraitDef('reservist',             'reserviste')
RESOLUTE            = CapaciteTraitDef('resolute',              'resolute')
SECURITY            = CapaciteTraitDef('security',              'security')
SIGINT              = CapaciteTraitDef('singint',               'sigint_close',         'sigint_far')
SNIPER              = CapaciteTraitDef('sniper',                'sniper',               'sniper_no_snipe')