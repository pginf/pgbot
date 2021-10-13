
from discord_slash import ComponentContext

from pgbot import PGBot, guild_ids
from pgbot.db.models import PGStudent
from pgbot.db.session import session

studentRole = 897450719190347806


async def on_component(ctx: ComponentContext):
    if ctx.channel_id != 897436666841661440:
        return

    if ctx.component.get("label") == "Odrzuć":
        await ctx.origin_message.delete()
        return

    embed = ctx.origin_message.embeds[0]

    fields = {field.name: field.value for field in embed.fields}

    student = session.query(PGStudent).filter_by(nr_albumu=int(fields.get('Numer albumu'))).first()

    if student:
        student.discord_id = int(fields.get("Discord ID"))

        await ctx.send("Jest już w bazie danych, uzupełniam discord ID")
    else:
        student = PGStudent(int(fields.get("Numer albumu")), fields.get("Imię"), fields.get("Nazwisko"), int(fields.get("Discord ID")))
        session.add(student)

        await ctx.send("Dodano do bazy danych")


def setup(bot: PGBot):
    bot.add_listener(on_component)
