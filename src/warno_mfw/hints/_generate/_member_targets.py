from ._member_def import MemberDef


TARGETS: dict[str, list[MemberDef]] = {
    'TTypeUnitModuleDescriptor': [
        MemberDef('Nationalite', 'ENationalite/'),
        MemberDef('MotherCountry'),
        MemberDef('AcknowUnitType', '~/TAcknowUnitType_'),
        MemberDef('TypeUnitFormation')
    ],
    'TProductionModuleDescriptor': [
        MemberDef('Factory', 'EDefaultFactories/')
    ],
    'TUnitUIModuleDescriptor': [
        MemberDef('UnitRole'),
        MemberDef('InfoPanelConfigurationToken'),
        MemberDef('TypeStrategicCount', 'ETypeStrategicDetailedCount/'),
        MemberDef('MenuIconTexture', 'Texture_RTS_H_'),
        MemberDef('SpecialtiesList', is_list_type=True)
    ]
}