from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from utils.ndf import ensure
from units._weapons import M16A2, M21, VIPER


def create(ctx: ModCreationContext) -> UnitRules | None:
    # FWD SUPPORT [EW]
    with ctx.create_infantry_unit("#RECO2 IEW TEAM", "US", "Scout_US", [(M16A2, 4), (M21, 1), (VIPER, 1)]) as iew_team:
        iew_team.modules.ui.edit_members(
            UpgradeFromUnit='d9_RECO2_FOLT_US',
            SpecialtiesList=['reco', '_gsr', '_jammer']
        )
        iew_team.modules.production.command_point_cost=80
        # add traits: EW, GSR, direction finding?
        iew_team.modules.append(ensure._object('TModuleSelector',
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