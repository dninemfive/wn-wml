from typing import Callable, Iterable, Self

from ndf_parse import Mod
from ndf_parse.model import List, ListRow, MemberRow, Object
from ndf_parse.model.abc import CellValue

from warno_mfw.hints import paths

from ...utils.types.message import Message, try_nest
from ._file_target import FileTarget
from ._member_def import MemberDef

def _select_unit_modules(row: ListRow) -> Iterable[Object]:
    for module_row in row.value.by_member('ModulesDescriptors').value:
        module = module_row.value
        if isinstance(module, Object):
            yield module

UniteDescriptor = FileTarget(paths.Generated.Gameplay.Gfx.UniteDescriptor,
                             _select_unit_modules,
                             TTypeUnitModuleDescriptor=[
                                MemberDef('Nationalite', 'ENationalite/'),
                                MemberDef('MotherCountry'),
                                MemberDef('AcknowUnitType', '~/TAcknowUnitType_'),
                                MemberDef('TypeUnitFormation')
                            ],
                            TProductionModuleDescriptor=[
                                MemberDef('Factory', 'EDefaultFactories/')
                            ],
                            TUnitUIModuleDescriptor=[
                                MemberDef('UnitRole'),
                                MemberDef('InfoPanelConfigurationToken'),
                                MemberDef('TypeStrategicCount', 'ETypeStrategicDetailedCount/'),
                                MemberDef('MenuIconTexture', 'Texture_RTS_H_'),
                                MemberDef('SpecialtiesList', is_list_type=True)
                            ])