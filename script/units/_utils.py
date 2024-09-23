from ndf_parse.model import Map, MapRow, MemberRow, Object

import utils.ndf.ensure as ensure
import utils.ndf.edit as edit
from creators.unit import UnitCreator

# from CommonData\Gameplay\Constantes\InitialisationGameDistanceUnits.ndf
LBU_TO_GRU_CONVERSION_FACTOR = 2.92198967
# from CommonData\System\Globals.ndf
METRE = 26

# determined by trial and error, based on the in-game scale of 1/3.2 (inverted) times a fudge factor
# TODO: figure out how to determine this properly
MAGIC_NUMBER = 2.806 

def autonomy_to_fuel_move_duration(range_km: float, speed_kmph: float) -> float:
    # the 3600 factor is because FuelMoveDuration is in seconds
    return (range_km / MAGIC_NUMBER) * (3600 / speed_kmph)

def make_standard_squad_module(total_soldiers: int, num_weapon2: int) -> Object:
    result = Object('TInfantrySquadWeaponAssignmentModuleDescriptor')
    turret_index_map = Map()
    for i in range(num_weapon2):
        turret_index_map.add(ensure.maprow(str(i), [1]))
    for i in range(num_weapon2, total_soldiers - 1):
        turret_index_map.add(ensure.maprow(str(i), [0]))
    turret_index_map.add(ensure.maprow(str(total_soldiers - 1), [0, 2]))
    result.add(MemberRow(turret_index_map, 'InitialSoldiersToTurretIndexMap'))
    return result

def edit_standard_squad(squad: UnitCreator, num_rifles: int, num_SAWs: int, salvos_per_rifle: int, salvos_per_SAW: int) -> None:
    with squad.edit_weapons() as weapons:
        weapons.edit_members(Salves=[salvos_per_rifle*num_rifles,salvos_per_SAW*num_SAWs,4])
        edit.members(weapons.get_turret_weapon(0,0), NbWeapons=num_rifles)
        edit.members(weapons.get_turret_weapon(1,0), NbWeapons=num_SAWs)
    squad_size = num_rifles + num_SAWs
    with squad.module_context('TBaseDamageModuleDescriptor') as damage_module:
        damage_module.edit_members(MaxPhysicalDamages=squad_size)
    with squad.module_context('GroupeCombat', by_name=True) as groupe_combat:
        edit.members(groupe_combat.object.by_member('Default').value, NbSoldatInGroupeCombat=squad_size)
    squad.replace_module('TInfantrySquadWeaponAssignmentModuleDescriptor', make_standard_squad_module(squad_size, num_SAWs))
    with squad.module_context('TTacticalLabelModuleDescriptor') as label_module:
        label_module.edit_members(NbSoldiers=squad_size)
        # todo: edit bounding box size?

def insert_between(unit: UnitCreator, first: Object, second: Object) -> None:
    # make unit upgrade from first
    # make second upgrade from unit
    raise NotImplemented