from context.mod_creation_context import ModCreationContext
from metadata.unit_rules import UnitRules
from context.module_context import ModuleContext
from units._utils import METRE
from utils.ndf import ensure

FLIGHT_ALTITUDE = 3000 / 3.2 * METRE
FLIGHT_SPEED = 200
DRAGONFLY = 'A37B_Dragonfly_US'

def create(ctx: ModCreationContext) -> UnitRules | None:
    # E-2C HAWKEYE
    with ctx.create_unit("#RECO1 RQ-2 PIONEER", "US", DRAGONFLY, button_texture_src_path='img/units/rq_2_pioneer/icon.png') as rq_2_pioneer:
        with rq_2_pioneer.module_context('AirplanePositionModuleDescriptor') as position_module:
            position_module.edit_members(LowAltitudeFlyingAltitude=FLIGHT_ALTITUDE)
        with rq_2_pioneer.module_context('GenericMovement', True) as generic_movement_module:
            generic_movement_module.object.by_member('Default').value.by_member('MaxSpeedInKmph').value = FLIGHT_SPEED
        # copy MiG-27M airplane module for maneuverability (worst maneuverability in the game, apparently)
        rq_2_pioneer.replace_module_from('MiG_27M_bombe_SOV', 'AirplaneMovement', True)
        with rq_2_pioneer.module_context('AirplaneMovement', True) as movement_module:
            # data from:
            #   https://www.aewa.org/Library/e2-info.html
            #   https://www.airvectors.net/ave2c.html
            #   https://web.archive.org/web/20051107221140/https://www.iss.northgrum.com/products/navy_products/e2c/e2c.html
            movement_module.edit_members(Altitude=FLIGHT_ALTITUDE,
                                         SpeedInKmph=FLIGHT_SPEED,
                                         OrderedAttackStrategies=['DogfightAttackStrategyDescriptor'])
        with rq_2_pioneer.module_context('TFuelModuleDescriptor') as fuel_module:
            fuel_module.edit_members(FuelCapacity=500, FuelMoveDuration=60)
        # lower hitpoints
        with rq_2_pioneer.module_context('TBaseDamageModuleDescriptor') as damage_module:
            damage_module.edit_members(MaxPhysicalDamages=3)
        # remove ECM
        with rq_2_pioneer.module_context('TDamageModuleDescriptor') as damage_module:
            damage_module.edit_members(HitRollECM=0.0)
        # increase stealth
        with rq_2_pioneer.module_context('TScannerConfigurationDescriptor') as scanner_module:
            # Dragonfly: 7000, Kiowa Warrior: 233.475
            scanner_module.edit_members(OpticalStrength=5000, OpticalStrengthAltitude=0)
            # remove air detection
            scanner_module.remove_member('SpecializedDetectionsGRU')
        with rq_2_pioneer.module_context('TReverseScannerWithIdentificationDescriptor') as reverse_scanner_module:
            visiblity_roll_rule = ensure._object('TModernWarfareVisibilityRollRule',
                                                 # EF-111A: 0.6, Dragonfly: 1.0, Kiowa: 0.73
                                                 IdentifyBaseProbability=0.73)
            reverse_scanner_module.edit_members(VisibilityRollRule=visiblity_roll_rule)
        with rq_2_pioneer.module_context('TProductionModuleDescriptor') as production_module:
            production_module.object.by_member('ProductionRessourcesNeeded').value.by_key('$/GFX/Resources/Resource_CommandPoints').value = 60
        # fast to arrive and evac since it's theoretically deployed on the battlefield
        rq_2_pioneer.replace_module('TAirplaneModuleDescriptor', ensure._object('TAirplaneModuleDescriptor',
                                                                               EvacuationTime=5,
                                                                               TravelDuration=5))
        # remove weapons
        rq_2_pioneer.remove_module('WeaponManager', by_name=True)
        rq_2_pioneer.remove_module('MissileCarriage', by_name=True)
        # make stealthy
        # F117: 3.0
        with rq_2_pioneer.module_context('TVisibilityModuleDescriptor') as visibility_module:
            visibility_module.edit_members(UnitConcealmentBonus=3.5)
        # change tags
        rq_2_pioneer.edit_ui_module(
            SpecialtiesList=ensure._list("'reco'"),
            MenuIconTexture="'Texture_RTS_H_reco'",
            TypeStrategicCount = 'ETypeStrategicDetailedCount/Reco_Hel'
        )
        # set orders to that of an unarmed aircraft
        ef_111 = rq_2_pioneer.get_other_unit('EF111_Raven_US')
        rq_2_pioneer.replace_module_from(ef_111, 'TOrderConfigModuleDescriptor')
        rq_2_pioneer.replace_module_from(ef_111, 'TOrderableModuleDescriptor')
        # make OA-37B upgrade from this
        with ModuleContext(rq_2_pioneer.get_other_unit(DRAGONFLY), 'TUnitUIModuleDescriptor') as dragonfly_ui:
            dragonfly_ui.edit_members(UpgradeFromUnit=ensure.unit_descriptor('d9_RECO1_RQ2_PIONEER_US'))
        return UnitRules(rq_2_pioneer, 1, [8, 0, 0, 0])