from typing import Iterable

from ndf_parse import Mod
from ndf_parse.model import ListRow, Object

from ...hints import paths
from ...utils.types.message import Message

from ._file_target import FileTarget
from ._member_def import MemberDef, _specialties_list_formatter

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
                                MemberDef('SpecialtiesList', special_formatter=_specialties_list_formatter)
                            ])

MissileCarriage = FileTarget(paths.Generated.Gameplay.Gfx.MissileCarriage,
                             TMissileCarriageConnoisseur=[
                                 MemberDef('PylonSet', '~/DepictionPylonSet_')
                             ])

TARGET_SETS = sorted([UniteDescriptor, MissileCarriage], key=lambda x: x.file_path)

def _add_all(mod: Mod, msg: Message) -> None:
    with msg.nest('Generating literals from files') as msg:
        for target_set in TARGET_SETS:
            target_set.add_all(mod, msg)