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

