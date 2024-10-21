import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from creators.unit.basic import BasicUnitCreator
from ndf_parse.model import ListRow, Map, MapRow, MemberRow, Object

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

def Metre(n: int) -> str:
    return f'(({n}) * Metre)'

def is_sell_module(row: ListRow) -> bool:
            if isinstance(row.value, Object):
                if row.value.type == 'TModuleSelector':
                    default = row.value.by_member("Default", strict=False)
                    if isinstance(default, MemberRow):
                        if(isinstance(default.value, Object)):
                            return default.value.type == 'TSellModuleDescriptor'
            return False                        