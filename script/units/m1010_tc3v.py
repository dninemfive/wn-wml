from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.division_unit_registry import UnitInfo
from ndf_parse.model import List
import ndf_paths as paths

def create(ctx: UnitCreationContext) -> UnitInfo | None:
    # ✪ M1010 TC3V
    with ctx.create_unit("#CMD ", "US", "M35_trans_US") as m1010_tc3v: # 🏳️‍⚧️
        # acknow type = cmd
        with m1010_tc3v.module_context("TTypeUnitModuleDescriptor") as unit_type_module:
            unit_type_module.edit_members(AcknowUnitType="~/TAcknowUnitType_Command",
                                          TypeUnitFormation="'Supply'")
        # add command tags:
        #   AllowedForMissileRoE
        #   Commandant
        #   InfmapCommander
        #   Vehicule_CMD
        m1010_tc3v.add_tags("AllowedForMissileRoE", "Commandant", "InfmapCommander", "Vehicule_CMD")
        # remove "Vehicule_Transport"
        m1010_tc3v.remove_tag("Vehicule_Transport")
        vlra = ctx.ndf[paths.UNITE_DESCRIPTOR].by_name("Descriptor_Unit_VLRA_trans_FR").value
        # model of VLRA
        with m1010_tc3v.module_context('ApparenceModel', by_name=True) as apparence_model:
             
        # damage of VLRA
        # movement of M35
        # larger command radius than usual
        # upgrades from ✪ M1025 AGL
        # m1075_pls.edit_ui_module(UpgradeFromUnit="Descriptor_Unit_d9_CMD_M1025_AGL_CMD_US")
        return UnitInfo(m1010_tc3v, 1, [0, 3, 2, 0])