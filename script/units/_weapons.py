from model.squads.infantry_weapon import InfantryWeapon

M16A2       = InfantryWeapon('$/GFX/Weapon/Ammo_FM_M16',
                             "'FireEffect_FM_M16'",
                             '$/GFX/DepictionResources/Modele_M16A2',
                             26)
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