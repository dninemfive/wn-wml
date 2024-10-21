
from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # M966 HUMVEE TOW
    with ctx.create_unit("M966 HUMVEE TOW", "US", "M1025_Humvee_TOW_US") as m966_humvee_tow:
        with m966_humvee_tow.edit_weapons('M1025_Humvee_TOW_US') as weapons:
            weapons.edit_members(Salves=[6,])
            # TODO: coaxial M240
        m966_humvee_tow.modules.ui.UpgradeFromUnit='M274_Mule_ITOW_US'
        # insert before M1025 Humvee TOW
        ctx.get_unit('M1025_Humvee_TOW_US').modules.ui.UpgradeFromUnit = m966_humvee_tow
        return m966_humvee_tow
