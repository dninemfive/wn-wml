from context.mod_creation import ModCreationContext
from metadata.unit_rules import UnitRules
from context.unit_module import UnitModuleContext
from units._utils import METRE
from utils.ndf import ensure

FLIGHT_ALTITUDE = 3000 / 3.2 * METRE
FLIGHT_SPEED = 200
DRAGONFLY = 'A37B_Dragonfly_US'

def create(ctx: ModCreationContext) -> UnitRules | None:
    # E-2C HAWKEYE
    with ctx.create_unit("#RECO1 RQ-2 PIONEER", "US", DRAGONFLY, button_texture_src_path='img/units/rq_2_pioneer/icon.png') as rq_2_pioneer:
        # TODO: something to edit plane flight speed and altitude all in one go
        rq_2_pioneer.modules.edit_members('AirplanePositionModuleDescriptor', LowAltitudeFlyingAltitude=FLIGHT_ALTITUDE)
        rq_2_pioneer.modules.get('GenericMovement', True).by_member('Default').value.by_member('MaxSpeedInKmph').value = FLIGHT_SPEED
        # copy MiG-27M airplane module for maneuverability (worst maneuverability in the game, apparently)
        rq_2_pioneer.modules.replace_from('MiG_27M_bombe_SOV', 'AirplaneMovement', True)
        
        rq_2_pioneer.modules.edit_members('AirplaneMovement', True,
            Altitude=FLIGHT_ALTITUDE,
            SpeedInKmph=FLIGHT_SPEED,
            OrderedAttackStrategies=['DogfightAttackStrategyDescriptor']
        )
        rq_2_pioneer.modules.edit_members('TFuelModuleDescriptor', FuelCapacity=500, FuelMoveDuration=60)
        # lower hitpoints
        rq_2_pioneer.modules.edit_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=3)
        # remove ECM
        rq_2_pioneer.modules.edit_members('TDamageModuleDescriptor', HitRollECM=0.0)
        # increase stealth
        rq_2_pioneer.modules.edit_members('TScannerConfigurationDescriptor',
                                          # Dragonfly: 7000, Kiowa Warrior: 233.475
                                          OpticalStrength=5000,
                                          # remove air detection
                                          OpticalStrengthAltitude=0,
                                          SpecializedDetectionsGRU=None)
        rq_2_pioneer.modules.edit_members('TReverseScannerWithIdentificationDescriptor',
                                          VisibilityRollRule=ensure._object('TModernWarfareVisibilityRollRule',
                                                                            # EF-111A: 0.6, Dragonfly: 1.0, Kiowa: 0.73
                                                                            IdentifyBaseProbability=0.73))
        rq_2_pioneer.modules.production.command_point_cost = 60
        # fast to arrive and evac since it's theoretically deployed on the battlefield
        rq_2_pioneer.modules.replace('TAirplaneModuleDescriptor',
                                     ensure._object('TAirplaneModuleDescriptor',
                                                    EvacuationTime=5,
                                                    TravelDuration=5))
        # remove weapons
        rq_2_pioneer.modules.remove('WeaponManager', by_name=True)
        rq_2_pioneer.modules.remove('MissileCarriage', by_name=True)
        # make stealthy
        # F117: 3.0
        rq_2_pioneer.modules.edit_members('TVisibilityModuleDescriptor', UnitConcealmentBonus=3.5)
        # change tags
        rq_2_pioneer.modules.ui.edit_members(
            # once NORTHAG is out, add '_uav' (assuming i update my version of the 9ID at all 😭)
            SpecialtiesList=['reco'],
            MenuIconTexture='reco',
            TypeStrategicCount = 'Reco_Hel'
        )
        # set orders to that of an unarmed aircraft
        ef_111 = ctx.get_unit('EF111_Raven_US')
        rq_2_pioneer.modules.replace_from(ef_111, 'TOrderConfigModuleDescriptor')
        rq_2_pioneer.modules.replace_from(ef_111, 'TOrderableModuleDescriptor')
        # make OA-37B upgrade from this
        ctx.get_unit(DRAGONFLY).modules.ui.UpgradeFromUnit = 'd9_RECO1_RQ2_PIONEER_US'
        return UnitRules(rq_2_pioneer, 1, [8, 0, 0, 0])