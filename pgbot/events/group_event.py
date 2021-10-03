import discord
from discord import Member
from discord_slash import ComponentContext

from pgbot import PGBot


groups = [894213777527021628, 894213867473887294, 894213914307493890, 894213965930987530, 894213993554640906, 894214014312275998, 894214042527338507]

async def on_component(ctx: ComponentContext):
    if ctx.origin_message_id != 894226439476482078:
        return

    member: Member = ctx.guild.get_member(ctx.author_id)
    for role in member.roles:
        if role.id in groups:
            await ctx.send("Już jesteś w grupie", hidden=True)
            return

    picked_group = int(ctx.component.get("label"))
    role = ctx.guild.get_role(groups[picked_group - 1])
    await member.add_roles(role)
    await ctx.send(f"Pomyślnie dodano do grupy {picked_group}", hidden=True)

def setup(bot: PGBot):
    bot.add_listener(on_component)