from model.squads.infantry_weapon import InfantryWeapon

M16A2       = InfantryWeapon('$/GFX/Weapon/Ammo_FM_M16',
                             "'FireEffect_FM_M16'",
                             '$/GFX/DepictionResources/Modele_M16A2',
                             26)
M240        = InfantryWeapon('$/GFX/Weapon/Ammo_MMG_inf_M240B_7_62mm',
                             "'FireEffect_MMG_inf_M240B_7_62mm'",
                             '$/GFX/DepictionResources/Modele_M240B',
                             92,
                             'mmg')
M249        = InfantryWeapon('$/GFX/Weapon/Ammo_SAW_M249_5_56mm',
                             "'FireEffect_SAW_M249_5_56mm'",
                             '$/GFX/DepictionResources/Modele_M249',
                             92,
                             'mmg')
DRAGON      = InfantryWeapon('$/GFX/Weapon/Ammo_M47_DRAGON_II',
                             "'FireEffect_M47_DRAGON_II'",
                             '$/GFX/DepictionResources/Modele_M47_DRAGON_II',
                             6,
                             'bazooka',
                             is_secondary=True)
AT4         = InfantryWeapon('$/GFX/Weapon/Ammo_RocketInf_AT4_83mm',
                             "'FireEffect_RocketInf_AT4_83mm'",
                             '$/GFX/DepictionResources/Modele_AT_4',
                             4,
                             'bazooka')
# TODO: grab satchel charges
SATCHEL_CHARGE = None
# TODO: make ammo for M60E3
# TODO: make ammo for M203
# TODO: make ammo for M224