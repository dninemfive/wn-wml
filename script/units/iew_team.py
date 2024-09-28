from script.context.mod_creation import ModCreationContext
from script.context.unit_module import UnitModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
from utils.ndf import ensure
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._utils import edit_standard_squad
from units._weapons import M16A2, M21, VIPER
from script.creators.unit.infantry import InfantryUnitCreator


def create(ctx: ModCreationContext) -> UnitRules | None:
    # FWD SUPPORT [EW]
    with ctx.create_unit("#RECO2 IEW TEAM", "US", "Scout_US") as iew_team:
        # TODO: change weapon loadout
        squad: InfantryUnitCreator = InfantryUnitCreator.copy_parent(ctx.guids, iew_team, 'US', (M16A2, 4), (M21, 1), (VIPER, 1))
        squad.apply(ctx.ndf, iew_team.msg)
        squad.edit_unit(iew_team)
        # TODO: add traits: EW, GSR, direction finding?
        iew_team.UpgradeFromUnit='d9_RECO2_FOLT_US'
        iew_team.CommandPointCost=80
        with iew_team.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.edit_members(SpecialtiesList=["'reco'", "'_gsr'", "'_jammer'"])
        iew_team.append_module(ensure._object('TModuleSelector',
            Default=ensure._object('TCapaciteModuleDescriptor',
                                   DefaultSkillList=[
                                       '$/GFX/EffectCapacity/Capacite_GSR',
                                       '$/GFX/EffectCapacity/Capacite_GSR_no_GSR',
                                       '$/GFX/EffectCapacity/Capacite_jammer',
                                       '$/GFX/EffectCapacity/Capacite_jammer_arty'
                                   ]),
            Selection=['~/NilDescriptorIfCadavre']
        ))
        return UnitRules(iew_team, 3, [0, 6, 4, 0])