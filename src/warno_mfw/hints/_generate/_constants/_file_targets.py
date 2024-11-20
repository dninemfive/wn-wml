from typing import Iterable

from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, Object

from warno_mfw.utils.ndf import ensure
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

def _select_weapon_type(row: ListRow) -> Iterable[Object]:
    try:
        operators: List = row.value.by_member('Operators').value
        for operator_row in operators:
            operator: Object = operator_row.value
            conditional_tags: List = operator.by_member('ConditionalTags').value
            result = ensure.NdfObject('WeaponType_generated', WeaponType=[row.value[0] for row in conditional_tags])
            yield result
    except:
        pass

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
GeneratedDepictionInfantry = FileTarget(paths.Generated.Gameplay.Gfx.Infanterie.GeneratedDepictionInfantry,
                                        _select_weapon_type,
                                        WeaponType_generated=[
                                            MemberDef('WeaponType')
                                        ])

TARGET_SETS = sorted([UniteDescriptor, MissileCarriage, GeneratedDepictionInfantry], key=lambda x: x.file_path)

def _add_all(mod: Mod, msg: Message) -> None:
    with msg.nest('Generating literals from files') as msg:
        for target_set in TARGET_SETS:
            target_set.add_all(mod, msg)