# TODO: dynamically load these from annotations on loaded types?

ALL_UNITS_TACTIC        = rf"GameData\Generated\Gameplay\Gfx\AllUnitsTactic.ndf"
DECK_SERIALIZER         = rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf"
DIVISIONS               = rf"GameData\Generated\Gameplay\Decks\Divisions.ndf"
DIVISION_LIST           = rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf"
DIVISION_PACKS          = rf'GameData\Generated\Gameplay\Decks\DivisionPacks.ndf'
DIVISION_RULES          = rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf"
SHOWROOM_EQUIVALENCE    = rf'GameData\Generated\Gameplay\Gfx\ShowRoomEquivalence.ndf'
UNITE_DESCRIPTOR        = rf'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf'
DIVISION_TEXTURES       = rf'GameData\Generated\UserInterface\Textures\DivisionTextures.ndf'
AMMUNITION              = rf'GameData\Generated\Gameplay\Gfx\Ammunition.ndf'
WEAPON_DESCRIPTOR       = rf'GameData\Generated\Gameplay\Gfx\WeaponDescriptor.ndf'
MISSILE_CARRIAGE        = rf'GameData\Generated\Gameplay\Gfx\MissileCarriage.ndf'
AMMUNITION_MISSILES     = rf'GameData\Generated\Gameplay\Gfx\AmmunitionMissiles.ndf'
BUTTON_TEXTURES_UNITES  = rf'GameData\Generated\UserInterface\Textures\ButtonTexturesUnites.ndf'

ALL = set([ALL_UNITS_TACTIC,
           DECK_SERIALIZER,
           DIVISIONS,
           DIVISION_LIST,
           DIVISION_PACKS,
           DIVISION_RULES,
           SHOWROOM_EQUIVALENCE,
           UNITE_DESCRIPTOR,
           DIVISION_TEXTURES,
           AMMUNITION,
           WEAPON_DESCRIPTOR,
           BUTTON_TEXTURES_UNITES,
           MISSILE_CARRIAGE,
           AMMUNITION_MISSILES])