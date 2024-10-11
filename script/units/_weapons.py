from creators.unit.utils.infantry.weapon import InfantryWeapon

M16A2           = InfantryWeapon('$/GFX/Weapon/Ammo_FM_M16',
                                 "'FireEffect_FM_M16'",
                                 '$/GFX/DepictionResources/Modele_M16A2',
                                 26)
M240            = InfantryWeapon('$/GFX/Weapon/Ammo_MMG_inf_M240B_7_62mm',
                                 "'FireEffect_MMG_inf_M240B_7_62mm'",
                                 '$/GFX/DepictionResources/Modele_M240B',
                                 92,
                                 'mmg')
M249            = InfantryWeapon('$/GFX/Weapon/Ammo_SAW_M249_5_56mm',
                                 "'FireEffect_SAW_M249_5_56mm'",
                                 '$/GFX/DepictionResources/Modele_M249',
                                 92,
                                 'mmg')
DRAGON          = InfantryWeapon('$/GFX/Weapon/Ammo_M47_DRAGON_II',
                                 "'FireEffect_M47_DRAGON_II'",
                                 '$/GFX/DepictionResources/Modele_M47_DRAGON_II',
                                 6,
                                 'bazooka',
                                 is_secondary=True)
AT4             = InfantryWeapon('$/GFX/Weapon/Ammo_RocketInf_AT4_83mm',
                                 "'FireEffect_RocketInf_AT4_83mm'",
                                 '$/GFX/DepictionResources/Modele_AT_4',
                                 4,
                                 'bazooka',
                                 is_secondary=True)
SATCHEL_CHARGE = InfantryWeapon('$/GFX/Weapon/Ammo_Grenade_Satchel_Charge',
                                "'FireEffect_Grenade_Satchel_Charge'",
                                '$/GFX/DepictionResources/Modele_MainNue',
                                5,
                                'grenade',
                                is_secondary=True)
TOW_SCAT        = InfantryWeapon('$/GFX/Weapon/Ammo_ATGM_BGM71_TOW',
                                 "'FireEffect_M47_DRAGON_II'",
                                 '$/GFX/DepictionResources/Modele_M47_DRAGON_II',
                                 6,
                                 'bazooka',
                                 is_secondary=True)
M60E3           = InfantryWeapon('$/GFX/Weapon/Ammo_d9_M60E3',
                                 "'FireEffect_MMG_M60_7_62mm'",
                                 '$/GFX/DepictionResources/Modele_M60',
                                 92,
                                 'mmg')
COLT_COMMANDO   = InfantryWeapon('$/GFX/Weapon/Ammo_PM_M4_Carbine',
                                 "'FireEffect_PM_M4_Carbine'",
                                 '$/GFX/DepictionResources/Modele_M16A1_Carbine',
                                 20)
M21             = InfantryWeapon('$/GFX/Weapon/Ammo_Sniper_M14',
                                 "'FireEffect_Sniper_M14'",
                                 '$/GFX/DepictionResources/Modele_M14_Sniper',
                                 100)
VIPER           = InfantryWeapon('$/GFX/Weapon/Ammo_d9_FGR17_Viper',
                                 "'FireEffect_RocketInf_M72_LAW_66mm'",
                                 '$/GFX/DepictionResources/Modele_M72A4',
                                 4,
                                 'bazooka',
                                 is_secondary=True)
M203           = InfantryWeapon('$/GFX/Weapon/Ammo_d9_40mm_HEDP',
                                 "'FireEffect_Lance_grenade_Mk19_40mm'",
                                 '$/GFX/DepictionResources/Modele_Handflammpatrone',
                                 36,
                                 'bazooka',
                                 is_secondary=True)
# TODO: make ammo for M224