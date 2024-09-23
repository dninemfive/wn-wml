from context.mod_creation_context import ModCreationContext
from metadata.unit_rules import UnitRules
from ndf_parse.model import Object
from units._utils import METRE
from utils.ndf import ensure

FLIGHT_ALTITUDE = 9150 / 3.2 * METRE
FLIGHT_SPEED = 480

def create(ctx: ModCreationContext) -> UnitRules | None:
    # E-2C HAWKEYE
    with ctx.create_unit("#RECO3 E-2C HAWKEYE [EW]", "US", "EF111_Raven_US", button_texture_src_path='img/units/e2c_hawkeye/icon.png') as e2c_hawkeye:
        e2c_hawkeye.add_tags('Avion_Reco')
        e2c_hawkeye.remove_tags('Avion_SEAD')
        with e2c_hawkeye.module_context('AirplanePositionModuleDescriptor') as position_module:
            position_module.edit_members(LowAltitudeFlyingAltitude=FLIGHT_ALTITUDE)
        with e2c_hawkeye.module_context('GenericMovement', True) as generic_movement_module:
            generic_movement_module.object.by_member('Default').value.by_member('MaxSpeedInKmph').value = FLIGHT_SPEED
        # copy MiG-27M airplane module for maneuverability (worst maneuverability in the game, apparently)
        e2c_hawkeye.replace_module_from('MiG_27M_bombe_SOV', 'AirplaneMovement', True)
        with e2c_hawkeye.module_context('AirplaneMovement', True) as movement_module:
            # data from:
            #   https://www.aewa.org/Library/e2-info.html
            #   https://www.airvectors.net/ave2c.html
            #   https://web.archive.org/web/20051107221140/https://www.iss.northgrum.com/products/navy_products/e2c/e2c.html
            movement_module.edit_members(Altitude=FLIGHT_ALTITUDE,
                                         SpeedInKmph=FLIGHT_SPEED,
                                         OrderedAttackStrategies=['DogfightAttackStrategyDescriptor'])
        # change fuel capacity
        # TODO: this should be basically enough so that you can just barely have both one E-2C up at all times if you bring both cards
        with e2c_hawkeye.module_context('TFuelModuleDescriptor') as fuel_module:
            fuel_module.edit_members(FuelCapacity=4800, FuelMoveDuration=480)
        # lower hitpoints
        with e2c_hawkeye.module_context('TBaseDamageModuleDescriptor') as damage_module:
            damage_module.edit_members(MaxPhysicalDamages=6)
        # lower ECM somewhat?
        # change vision: sees ground pretty well, radar AA very well
        with e2c_hawkeye.module_context('TScannerConfigurationDescriptor') as scanner_module:
            # Dragonfly: 7000, Kiowa Warrior: 233.475
            scanner_module.edit_members(OpticalStrength=7000,
            # TODO: grant specialized optical strengths from Kiowa? Buff detection strength further? 
            # also TODO: get values from game units
                                         SpecializedDetectionsGRU={'EVisionUnitType/AlwaysInHighAltitude': 31802.0, 'EVisionUnitType/AntiRadar': 31802.0})
        with e2c_hawkeye.module_context('TReverseScannerWithIdentificationDescriptor') as reverse_scanner_module:
            visiblity_roll_rule = ensure._object('TModernWarfareVisibilityRollRule',
                                                 # EF-111A: 0.6, Dragonfly: 1.0, Kiowa: 0.73
                                                 IdentifyBaseProbability=1.0,
                                                 )
            reverse_scanner_module.edit_members(VisibilityRollRule=visiblity_roll_rule)
        # change tab: recon, cost: very high
        with e2c_hawkeye.module_context('TProductionModuleDescriptor') as production_module:
            production_module.edit_members(Factory='EDefaultFactories/Recons')
            production_module.object.by_member('ProductionRessourcesNeeded').value.by_key('$/GFX/Resources/Resource_CommandPoints').value = 300
        # v slow to arrive and evacuate
        e2c_hawkeye.replace_module('TAirplaneModuleDescriptor', ensure._object('TAirplaneModuleDescriptor',
                                                                               EvacuationTime=12,
                                                                               TravelDuration=13))
        # change tags
        e2c_hawkeye.edit_ui_module(
            SpecialtiesList=ensure._list("'reco'", "'_electronic_warfare'"),         # TODO: custom AWACS specialty?
            MenuIconTexture="'Texture_RTS_H_reco'",                                  # TODO: custom AWACS texture
            TypeStrategicCount = 'ETypeStrategicDetailedCount/Reco_Hel',
            UpgradeFromUnit=ensure.unit_descriptor('A37B_Dragonfly_US')
        )
        # TODO: remove EW module?
        return UnitRules(e2c_hawkeye, 2, [0, 1, 0, 0])