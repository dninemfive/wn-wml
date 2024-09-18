import constants.ndf_paths as ndf_paths
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UnitCreator
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow, Object
from utils.ndf import ensure


def create(ctx: ModCreationContext) -> UnitRules | None:
    # ✪ M1010 TC3V
    with ctx.create_unit("#CMD M1010 TC3V", "US", "M35_trans_US") as m1010_tc3v: # 🏳️‍⚧️
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
        edit_with_vlra(m1010_tc3v, get_unit(ctx, "VLRA_trans_FR"))
        # add command module
        # TODO: larger command radius than usual
        m1010_tc3v.append_module(ListRow(Object('TCommanderModuleDescriptor')))
        # remove capturable module
        m1010_tc3v.remove_module_where(lambda x: isinstance(x.value, str) and x.value == "~/CapturableModuleDescriptor")
        edit_with_m1025(m1010_tc3v, get_unit(ctx, "M1025_Humvee_CMD_US"))
        # remove transporter module
        m1010_tc3v.remove_module('Transporter', by_name=True)
        with m1010_tc3v.module_context('TProductionModuleDescriptor') as production_module:
            production_module.edit_members(Factory="EDefaultFactories/Logistic", 
                                           ProductionRessourcesNeeded={"$/GFX/Resources/Resource_CommandPoints": str(85),
                                                                       "$/GFX/Resources/Resource_Tickets":       str(1)})
        
        m1010_tc3v.append_module(Object('TInfluenceScoutModuleDescriptor'))

        def is_sell_module(row: ListRow) -> bool:
            if isinstance(row.value, Object):
                if row.value.type == 'TModuleSelector':
                    default = row.value.by_member("Default", strict=False)
                    if isinstance(default, Object):
                        return default.type == 'TSellModuleDescriptor'
            return False                        
        m1010_tc3v.remove_module_where(is_sell_module)
        # TODO: upgrades from ✪ M1025 AGL
        # m1075_pls.edit_ui_module(UpgradeFromUnit="Descriptor_Unit_d9_CMD_M1025_AGL_CMD_US")
        # TODO: modify fuel module
        with m1010_tc3v.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.remove_member('UpgradeFromUnit')
        m1010_tc3v.edit_ui_module(UnitRole="'tank_B'",
                                  SpecialtiesList=["'hq_veh'", "'_leader'"],
                                  InfoPanelConfigurationToken="'Default'",
                                  MenuIconTexture="'Texture_RTS_H_CMD_veh'",
                                  TypeStrategicCount='ETypeStrategicDetailedCount/CMD_Veh',
                                  ButtonTexture="'Texture_Button_Unit_VLRA_trans_FR'")
        # TODO: separate showroom model
        return UnitRules(m1010_tc3v, 1, [0, 3, 2, 0])
    
def get_unit(ctx: ModCreationContext, unit: str) -> Object:
    return ctx.ndf[ndf_paths.UNITE_DESCRIPTOR].by_name(f"Descriptor_Unit_{unit}").value
    
def edit_with_vlra(m1010_tc3v: UnitCreator, vlra: Object) -> None:
    # model of VLRA
    m1010_tc3v.replace_module_from(vlra, 'ApparenceModel', by_name=True)
    m1010_tc3v.replace_module_from(vlra, 'TCadavreGeneratorModuleDescriptor')
    m1010_tc3v.replace_module_from(vlra, 'TBaseDamageModuleDescriptor')
    
def edit_with_m1025(m1010_tc3v: UnitCreator, m1025_cmd: Object) -> None:
    # scanner from M1025 CMD
    m1010_tc3v.replace_module_from(m1025_cmd, 'TScannerConfigurationDescriptor')
    m1010_tc3v.replace_module_from(m1025_cmd, 'TemplateUnitCriticalModule')
    m1010_tc3v.replace_module_from(m1025_cmd, 'TScannerConfigurationDescriptor')                                        
    m1010_tc3v.replace_module_from(m1025_cmd, 'TCubeActionModuleDescriptor')
    # TODO: automatically generate new order descriptor for units
    m1010_tc3v.replace_module_from(m1025_cmd, 'TOrderConfigModuleDescriptor')
    m1010_tc3v.replace_module_from(m1025_cmd, 'TOrderableModuleDescriptor')
    m1010_tc3v.replace_module_from(m1025_cmd, 'TTacticalLabelModuleDescriptor')

    m1010_tc3v.append_module_from(m1025_cmd, 'TZoneInfluenceMapModuleDescriptor')