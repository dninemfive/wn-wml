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
    with ctx.create_unit("#RECO1 MQM-10 AQUILA", "US", DRAGONFLY, button_texture_src_path='img/units/rq_2_pioneer/icon.png') as mqm_10_aquila:
        # TODO: something to edit plane flight speed and altitude all in one go
        mqm_10_aquila.modules.edit_members('AirplanePositionModuleDescriptor', LowAltitudeFlyingAltitude=FLIGHT_ALTITUDE)
        mqm_10_aquila.modules.get('GenericMovement', True).by_member('Default').value.by_member('MaxSpeedInKmph').value = FLIGHT_SPEED
        # copy MiG-27M airplane module for maneuverability (worst maneuverability in the game, apparently)
        mqm_10_aquila.modules.replace_from('MiG_27M_bombe_SOV', 'AirplaneMovement', True)
        
        mqm_10_aquila.modules.edit_members('AirplaneMovement', True,
            Altitude=FLIGHT_ALTITUDE,
            SpeedInKmph=FLIGHT_SPEED,
            OrderedAttackStrategies=['DogfightAttackStrategyDescriptor']
        )
        mqm_10_aquila.modules.edit_members('TFuelModuleDescriptor', FuelCapacity=500, FuelMoveDuration=60)
        # lower hitpoints
        mqm_10_aquila.modules.edit_members('TBaseDamageModuleDescriptor', MaxPhysicalDamages=3)
        # remove ECM
        mqm_10_aquila.modules.edit_members('TDamageModuleDescriptor', HitRollECM=0.0)
        # increase stealth
        mqm_10_aquila.modules.edit_members('TScannerConfigurationDescriptor',
                                          # Dragonfly: 7000, Kiowa Warrior: 233.475
                                          OpticalStrength=5000,
                                          # remove air detection
                                          OpticalStrengthAltitude=0,
                                          SpecializedDetectionsGRU=None)
        mqm_10_aquila.modules.edit_members('TReverseScannerWithIdentificationDescriptor',
                                          VisibilityRollRule=ensure._object('TModernWarfareVisibilityRollRule',
                                                                            # EF-111A: 0.6, Dragonfly: 1.0, Kiowa: 0.73
                                                                            IdentifyBaseProbability=0.73))
        mqm_10_aquila.modules.production.command_point_cost = 60
        # fast to arrive and evac since it's theoretically deployed on the battlefield
        mqm_10_aquila.modules.replace('TAirplaneModuleDescriptor',
                                     ensure._object('TAirplaneModuleDescriptor',
                                                    EvacuationTime=5,
                                                    TravelDuration=5))
        # remove weapons
        mqm_10_aquila.modules.remove('WeaponManager', by_name=True)
        mqm_10_aquila.modules.remove('MissileCarriage', by_name=True)
        # TODO: update depiction and showroom unit
        # - remove Operators:
        #   - DepictionOperator_Turret1_Aim
        #   - Op_A37B_Dragonfly_US_Weapon*
        #   - flares?
        # - remove Actions:
        #   - ones with weapon effet tags
        # make stealthy
        # F117: 3.0
        mqm_10_aquila.modules.edit_members('TVisibilityModuleDescriptor', UnitConcealmentBonus=3.5)
        # change tags
        mqm_10_aquila.modules.ui.edit_members(
            # once NORTHAG is out, add '_uav' (assuming i update my version of the 9ID at all 😭)
            SpecialtiesList=['reco'],
            MenuIconTexture='reco',
            TypeStrategicCount = 'Reco_Hel'
        )
        # set orders to that of an unarmed aircraft
        ef_111 = ctx.get_unit('EF111_Raven_US')
        mqm_10_aquila.modules.replace_from(ef_111, 'TOrderConfigModuleDescriptor')
        mqm_10_aquila.modules.replace_from(ef_111, 'TOrderableModuleDescriptor')
        # make OA-37B upgrade from this
        ctx.get_unit(DRAGONFLY).modules.ui.UpgradeFromUnit = mqm_10_aquila
        return UnitRules(mqm_10_aquila, 1, [8, 0, 0, 0])