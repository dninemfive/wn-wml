from context.mod_creation import ModCreationContext
from metadata.unit_rules import UnitRules
from ndf_parse.model import Object
from units._utils import METRE
from utils.ndf import ensure

FLIGHT_ALTITUDE = 9150 / 3.2 * METRE
FLIGHT_SPEED = 480

def create(ctx: ModCreationContext) -> UnitRules | None:
    # E-2C HAWKEYE
    with ctx.create_unit("#RECO3 E-2C HAWKEYE [EW]", "US", "EF111_Raven_US", button_texture_src_path='img/units/e2c_hawkeye/icon.png') as e2c_hawkeye:
        e2c_hawkeye.tags.add('Avion_Reco')
        e2c_hawkeye.tags.remove('Avion_SEAD')
        e2c_hawkeye.modules.edit_members('AirplanePositionModuleDescriptor', LowAltitudeFlyingAltitude=FLIGHT_ALTITUDE)
        e2c_hawkeye.modules.get('GenericMovement', True).by_member('Default').value.by_member('MaxSpeedInKmph').value = FLIGHT_SPEED
        # copy MiG-27M airplane module for maneuverability (worst maneuverability in the game, apparently)
        e2c_hawkeye.modules.replace_from('MiG_27M_bombe_SOV', 'AirplaneMovement', True)
        # data from:
        #   https://www.aewa.org/Library/e2-info.html
        #   https://www.airvectors.net/ave2c.html
        #   https://web.archive.org/web/20051107221140/https://www.iss.northgrum.com/products/navy_products/e2c/e2c.html
        e2c_hawkeye.modules.edit_members('AirplaneMovement', True,
                                            Altitude=FLIGHT_ALTITUDE,
                                            SpeedInKmph=FLIGHT_SPEED,
                                            OrderedAttackStrategies=['DogfightAttackStrategyDescriptor'])
        # change fuel capacity
        # TODO: this should be basically enough so that you can just barely have both one E-2C up at all times if you bring both cards
        e2c_hawkeye.modules.edit_members('TFuelModuleDescriptor',
                                         FuelCapacity=4800,
                                         FuelMoveDuration=480)
        # lower hitpoints
        # TODO: TBaseDamageModuleDescriptor wrapper
        e2c_hawkeye.modules.edit_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=6)
        # lower ECM somewhat?
        # change vision: sees ground pretty well, radar AA very well
        e2c_hawkeye.modules.edit_members('TScannerConfigurationDescriptor',
                                        # Dragonfly: 7000, Kiowa Warrior: 233.475
                                         OpticalStrength=7000,
                                        # TODO: grant specialized optical strengths from Kiowa? Buff detection strength further? 
                                        # also TODO: get values from game units
                                         SpecializedDetectionsGRU={'EVisionUnitType/AlwaysInHighAltitude': 31802.0, 'EVisionUnitType/AntiRadar': 31802.0})
        e2c_hawkeye.modules.edit_members('TReverseScannerWithIdentificationDescriptor',
                                         VisibilityRollRule=ensure._object('TModernWarfareVisibilityRollRule',
                                                                           # EF-111A: 0.6, Dragonfly: 1.0, Kiowa: 0.73
                                                                           IdentifyBaseProbability=1.0))
        # change tab: recon, cost: very high
        e2c_hawkeye.modules.production.edit_members(
            Factory = 'Recons',
            command_point_cost = 300
        )
        # v slow to arrive and evacuate
        e2c_hawkeye.modules.replace('TAirplaneModuleDescriptor',
                                    ensure._object('TAirplaneModuleDescriptor',
                                                   EvacuationTime=12,
                                                   TravelDuration=13))
        # change tags
        # TODO: automate specialties list
        e2c_hawkeye.modules.ui.edit_members(
            SpecialtiesList=['reco', '_electronic_warfare'],         # TODO: custom AWACS specialty?
            MenuIconTexture='reco',                                  # TODO: custom AWACS texture
            TypeStrategicCount = 'Reco_Hel',
            UpgradeFromUnit='A37B_Dragonfly_US'
        )
        # TODO: remove EW module?
        return UnitRules(e2c_hawkeye, 2, [0, 1, 0, 0])