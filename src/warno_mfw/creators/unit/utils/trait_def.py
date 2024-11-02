from typing import Self

from ndf_parse.model import List, Object
import warno_mfw.utils.ndf.ensure as ensure

# TODO: way to define this to include other ways of implementing traits (e.g. forward deployment, corrected accuracy)?
# e.g. CapaciteTraitDef: current
#      BaseTraitDef: abstract edit()
class TraitDef(object):
    def __init__(self: Self, icon_tag: str, *capacites: str):
        self.icon_tag = ensure.quoted(ensure.prefix(icon_tag, '_'))
        self.capacites = [ensure.prefix(x, '$/GFX/EffectCapacity/Capacite_') for x in capacites]

    def edit_capacite_module(self: Self, capacite_module: Object) -> None:
        default_skills: List = capacite_module.by_member('DefaultSkillList').value
        skills = sorted(set([x.value for x in default_skills] + self.capacites))
        capacite_module.by_member('DefaultSkillList').value = ensure._list(skills)

    def edit_ui_module(self: Self, ui_module: Object) -> None:
        specialties_list: List = ui_module.by_member('SpecialtiesList').value
        if self.icon_tag not in [x.value for x in specialties_list]:
            specialties_list.add(ensure.listrow(self.icon_tag))