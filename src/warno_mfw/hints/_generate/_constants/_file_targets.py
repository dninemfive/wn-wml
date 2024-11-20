from typing import Iterable

from ndf_parse import Mod
from ndf_parse.model import ListRow, Object

from warno_mfw.utils.types.message import Message
from ... import paths
from .._types._file_target import FileTarget
from .._types._member_def import MemberDef
from ._specialties_list_generators import (
    _specialties_list_literal_generator, _specialties_list_resolver_generator)


def _select_unit_modules(row: ListRow) -> Iterable[Object]:
    for module_row in row.value.by_member('ModulesDescriptors').value:
        module = module_row.value
        if isinstance(module, Object):
            yield module

UniteDescriptor = FileTarget(paths.Generated.Gameplay.Gfx.UniteDescriptor,
                             _select_unit_modules,
                             TTypeUnitModuleDescriptor=[
                                MemberDef('Nationalite', 'ENationalite/',
                                          aliases={
                                              'Axis': 'PACT',
                                              'Allied': 'NATO'
                                          }),
                                MemberDef('MotherCountry', enum=False),
                                MemberDef('AcknowUnitType', '~/TAcknowUnitType_'),
                                MemberDef('TypeUnitFormation')
                            ],
                            TProductionModuleDescriptor=[
                                MemberDef('Factory', 'EDefaultFactories/',
                                          aliases={
                                              'Art':        'ART',
                                              'DCA':        'AA',
                                              'Helis':      'HEL',
                                              'Infantry':   'INF',
                                              'Logistic':   'LOG',
                                              'Planes':     'AIR',
                                              'Recons':     'REC',
                                              'Tanks':      'TNK'
                                          })
                            ],
                            TUnitUIModuleDescriptor=[
                                MemberDef('UnitRole'),
                                MemberDef('InfoPanelConfigurationToken'),
                                MemberDef('TypeStrategicCount', 'ETypeStrategicDetailedCount/'),
                                MemberDef('MenuIconTexture', 'Texture_RTS_H_', enum=False),
                                MemberDef('SpecialtiesList',
                                          literal_generator=_specialties_list_literal_generator,
                                          resolver_generator=_specialties_list_resolver_generator)
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