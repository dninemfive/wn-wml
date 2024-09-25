from typing import Self
from ndf_parse.model import Object

def adjust_squad(squad: Object, *loadouts: tuple[int, list[str] | list[str]]) -> None:
    # for loadout in loadouts
    # add tuple[1] ct of soldiers (default 1 if ct not included) with the specified loadout
    # create custom gfx depiction based on this
    # create showroom unit
    raise NotImplemented
    # things which need to be changed:
    # ApparenceModel
    # new TemplateAllSubWeaponDepiction
    # WeaponManager -> new WeaponDescriptor
    # TBaseDamageModuleDescriptor.MaxPhysicalDamages = sum(k for k in loadouts)
    # TDangeroussnessModuleDescriptor proportional to weapons and size
    # GroupeCombat.Default.NbSoldatInGroupeCombat = ct
    # TacticalLabelModuleDescriptor
    # bounding box

class Weapon(object):
    def __init__(self: Self, ammo_path: str, effect_tag: str, model_path: str, meshless_path: str | None = None):
        self.ammo_path = ammo_path
        self.effect_tag = effect_tag
        self.model_path = model_path
        self.meshless_path = meshless_path if meshless_path is not None else model_path

class Squad(object):
    def __init__(self: Self, *loadout: Weapon | list[Weapon] | tuple[int, list[Weapon]]):
        self.loadout: list[list[str]] = []
        for item in loadout:
            if isinstance(item, Weapon):
                item = [item]
            if isinstance(item, list):
                item = (1, item)
            ct, weapons = item
            for i in range(ct):
                self.loadout.append(weapons)

    @property
    def total_soldiers(self: Self) -> int:
        return len(self.loadout)