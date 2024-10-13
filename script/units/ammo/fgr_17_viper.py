from __future__ import annotations

from context.mod_creation import ModCreationContext


def create(ctx: ModCreationContext) -> str:
    with ctx.create_ammo('Ammo_d9_FGR17_Viper', 'Ammo_RocketInf_M72A1_LAW_66mm') as creator:
        creator.edit_members(Name=ctx.localization.register('FGR-17 Viper'),
                             Caliber=ctx.localization.register('70mm'),
                             PorteeMaximaleTBAGRU=300)
        # TODO: custom texture