from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule
from utils.ndf import dict_to_map

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
    # ✪ MOT. RIFLES LDR.
    # copy: Airborne Ldr.
    with ctx.create_unit("MOT. RIFLES LDR.", "US", "Airborne_CMD_US") as mot_rifles_ldr:# MOT. RIFLES (AT-4)
        with ctx.create_unit("MOT. RIFLES (AT-4)", "Rifles_half_AT4_US") as mot_rifles:
            # change number of guys to 8
            # TODO: figure out appropriate dangerousness, bounding box size, command point cost
            with ModuleContext(mot_rifles.unit_object, "TBaseDamageModuleDescriptor") as base_damage_module:
                base_damage_module.edit_members(MaxPhysicalDamages=8)
            mot_rifles.unit_object.by_member("ModulesDescriptors").value.by_name("WeaponManager").value.by_member("NbSoldatInGroupeCombat").value = 8
            with ModuleContext(mot_rifles.unit_object, "TTacticalLabelModuleDescriptor") as tactical_label_module:
                tactical_label_module.edit_members(NbSoldiers=8)
            with ModuleContext(mot_rifles.unit_object, "TInfantrySquadWeaponAssignmentModuleDescriptor") as weapon_assignment_module:
                # TODO: simplify this since most squads follow the same general pattern
                weapon_assignment_module.edit_members(InitialSoldiersToTurretIndexMap=dict_to_map(
                    {
                        (
                                0, [1]
                        ),
                        (
                                1, [1]
                        ),
                        {
                                2, [0]
                        },
                        {
                                3, [0]
                        },
                        {
                                4, [0]
                        },
                        {
                                5, [0]
                        },
                        {
                                6, [0]
                        },
                        {
                                7, [0]
                        },
                        {
                                8, [0, 2]
                        }
                    }
                ))
            # remove Infanterie_IFV from tags?
            # change TTransportableModuleDescriptor
            # change UI module
            with ModuleContext(mot_rifles.unit_object, "TUnitUIModuleDescriptor") as ui_module:
                # TODO: upgrade from cmd. mot. rifles
                ui_module.remove_member("UpgradeFromUnit")
        rule = TDeckUniteRule(
            mot_rifles_ldr.new.descriptor_path,
            AvailableWithoutTransport=False,
            # TODO: decide on transports
            AvailableTransportList=["$/GFX/Unit/Descriptor_Unit_M998_Humvee_US"],
            # TODO: automatically get this from Airborne CMD
            NumberOfUnitInPack=6,
            # unit rule xp should also be higher
            NumberOfUnitInPackXPMultiplier=[0, 1, 0.6, 0]
        )
        return ((mot_rifles_ldr.new.deck_pack_descriptor_path, 2), rule)
        