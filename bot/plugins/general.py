from hikari.interactions.base_interactions import ResponseType
from hikari.messages import MessageFlag
import hikari
from hikari import ButtonStyle
import time
import typing
from lightbulb import Plugin, commands
import lightbulb
from lightbulb.context.slash import SlashContext
from bot.bot import Bot
from bot.database import DB
from bot.utils import Prayer
from bot.utils import command_error


general_plugin = Plugin("general")

@general_plugin.command()
@lightbulb.command("ping", "سرعة اتصال البوت")
@lightbulb.implements(commands.SlashCommand)
async def ping(ctx: SlashContext):
    await ctx.interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    before = time.monotonic()
    embed = hikari.Embed(color=0xffd430)
    embed.set_footer(
        text="بوت فاذكروني لإحياء سنة ذكر الله",
        icon=ctx.bot.get_me().avatar_url
    )
    embed.set_thumbnail(ctx.bot.get_me().avatar_url)
    embed.description = "```\nping\n```"
    await ctx.interaction.edit_initial_response(embed=embed)
    ping = (time.monotonic() - before) * 1000

    embed.description = "```python\nTime: %s ms\nLatency: %s ms\nDatabase: %s ms\n```" % (
        int(ping), round(ctx.bot.heartbeat_latency * 1000),
        ctx.bot.db.speed_test()
    )
    await ctx.interaction.edit_initial_response(embed=embed)

@general_plugin.command()
@lightbulb.command("support", "طلب الدعم الفني")
@lightbulb.implements(commands.SlashCommand)
async def support(ctx: SlashContext):
    await ctx.interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    embed = hikari.Embed(
        title="**شكرا على اختيارك بوت فاذكروني 🌹**",
        color=0xffd430
    )
    embed.set_footer(
        text="بوت فاذكروني لإحياء سنة ذكر الله",
        icon=ctx.bot.get_me().avatar_url
    )
    buttons = ctx.bot.rest.build_action_row()
    buttons = (
        buttons.add_button(
            ButtonStyle.LINK, f"https://discord.com/oauth2/authorize?client_id={ctx.bot.get_me().id}&permissions=8&scope=bot%20applications.commands")
        .set_label("أضافة البوت")
        .add_to_container()
    )
    buttons = (
        buttons.add_button(
            ButtonStyle.LINK, "https://discord.gg/VX5F54YNuy")
        .set_label("الدعم الفني")
        .add_to_container()
    )
    buttons = (
        buttons.add_button(ButtonStyle.LINK, "https://fdrbot.xyz/paypal")
        .set_label("التبرع")
        .add_to_container()
    )
    embed.set_thumbnail(ctx.bot.get_me().avatar_url)
    await ctx.interaction.edit_initial_response(embed=embed, component=buttons)

@general_plugin.command()
@lightbulb.command("info", "طلب معلومات الخادم")
@lightbulb.implements(commands.SlashCommand)
async def info(ctx: SlashContext):
    await ctx.interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    data = ctx.bot.db.fetch_guild(ctx.guild_id)
    times = {1800: "30m", 3600: "1h", 7200: "2h",
             21600: "6h", 43200: "12h", 86400: "24h"}
    hashtag = await ctx.bot.emojis.hashtag
    ping = await ctx.bot.emojis.ping
    off = await ctx.bot.emojis.off
    on = await ctx.bot.emojis.on

    embed = hikari.Embed(
        description="إعدادات خادم: %s" % ctx.get_guild().name,
        color=0xffd430
    )
    embed.add_field(
        name="%s - البادئه:" % hashtag,
        value=data.prefix,
        inline=True
    )
    embed.add_field(
        name="%s - روم الاذكار:" % hashtag,
        value=ctx.bot.cache.get_guild_channel(
            data.channel_id).mention if data.channel_id is not None else "لا يوجد",
        inline=True
    )
    embed.add_field(
        name="%s - وقت ارسال الاذكار:" % hashtag,
        value=times.get(data.time),
        inline=True
    )
    embed.add_field(
        name="%s - وضع تكرار الرسائل:" % hashtag,
        value=on if data.anti_spam else off,
        inline=True
    )
    embed.add_field(
        name="%s - وضع الامبد:" % hashtag,
        value=on if data.embed else off,
        inline=True
    )
    embed.add_field(
        name="%s - ايدي الشارد:" % hashtag,
        value=str(ctx.get_guild().shard_id),
        inline=True)

    embed.add_field(
        name="%s - سرعه الشارد:" % hashtag,
        value=f"{round(ctx.bot.shards.get(ctx.get_guild().shard_id) .heartbeat_latency * 1000)}ms {ping}",
        inline=True
    )
    embed.set_footer(text=ctx.bot.footer, icon=ctx.bot.get_me().avatar_url)
    embed.set_thumbnail(ctx.bot.get_me().avatar_url)
    await ctx.interaction.edit_initial_response(embed=embed)

@general_plugin.command()
@lightbulb.option(description="الدولة المراد معرفه وقت الصلاة بيها", name="المدينة", required=True)
@lightbulb.command("azan", "معرفة وقت الأذان في المدينة الخاصه بك")
@lightbulb.implements(commands.SlashCommand)
async def azan(ctx: SlashContext):
    country = ctx.raw_options.get("المدينة")
    embed = hikari.Embed(color=0xffd430)
    prayer = Prayer(country=country)
    x = prayer.country()
    if isinstance(x, dict):
        x = prayer.city()
        if isinstance(x, dict):
            return await command_error(ctx, "لم استطع العثور على المدينه او الدوله")
    embed.set_author(name=x.description, url=x.url)
    embed.add_field(name="صلاة الفجْر", value=x.fjer, inline=True)
    embed.add_field(name="الشروق", value=x.sunrise, inline=True)
    embed.add_field(name="صلاة الظُّهْر", value=x.noon, inline=True)
    embed.add_field(name="صلاة العَصر", value=x.pressing, inline=True)
    embed.add_field(name="صلاة المَغرب", value=x.moroccan, inline=True)
    embed.add_field(name="صلاة العِشاء", value=x.isha, inline=True)
    embed.set_footer(text=ctx.bot.footer)
    embed.set_thumbnail(ctx.bot.get_me().avatar_url)
    await ctx.interaction.create_initial_response(ResponseType.MESSAGE_CREATE, embed=embed)

@general_plugin.command()
@lightbulb.command("bot", "جلب معلومات البوت")
@lightbulb.implements(commands.SlashCommand)
async def bot(ctx: SlashContext):
    await ctx.interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    hashtag = await ctx.bot.emojis.hashtag

    guilds_count = len(ctx.bot.cache.get_guilds_view())

    embed = hikari.Embed(
        color=0xffd430,
        description=ctx.bot.get_me().username,
        url="http://fdrbot.xyz/invite"
    )
    embed.add_field(
        name="%s - الخوادم" % hashtag,
        value="{:,}".format(guilds_count),
        inline=True
    )
    embed.add_field(
        name="%s - تأخير الأستجابه" % hashtag,
        value="%sms" % round(ctx.bot.heartbeat_latency * 1000),
        inline=True
    )
    embed.add_field(
        name="%s - سرعة استجابة قواعد البيانات" % hashtag,
        value="%sms" % ctx.bot.db.speed_test(),
        inline=True
    )
    embed.add_field(
        name="%s - أصدار النسخة" % hashtag,
        value="V3.0.0",
        inline=True
    )
    embed.add_field(
        name="%s - الشاردات" % hashtag,
        value="%s/%s" % (
             len(ctx.bot.shards),
             len([shard for shard in ctx.bot.shards.values() if shard.is_alive])
        ),
        inline=True
    )
    embed.add_field(
        name="%s - أصدار المكتبة" % hashtag,
        value="`hikari %s`" % hikari.__version__,
        inline=True
    )
    embed.set_footer(text=ctx.bot.footer, icon=ctx.bot.get_me().avatar_url)
    embed.set_thumbnail(ctx.bot.get_me().avatar_url)
    await ctx.interaction.edit_initial_response(embed=embed)

@general_plugin.command()
@lightbulb.command("invite", "أضافة البوت إلى خادمك")
@lightbulb.implements(commands.SlashCommand)
async def invite(ctx: SlashContext):
    await ctx.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        f"<https://discord.com/oauth2/authorize?client_id={ctx.bot.get_me().id}&permissions=8&scope=bot%20applications.commands>",
        flags=MessageFlag.EPHEMERAL
    )

@general_plugin.command()
@lightbulb.command("zker", "ارسال ذكر عشوائي")
@lightbulb.implements(commands.SlashCommand)
async def zker(ctx: SlashContext):
    random_zker = ctx.bot.db.get_random_zker()
    embed = hikari.Embed(
        title=str(random_zker.id),
        description=random_zker.content,
        color=0xffd430
    )
    embed.set_footer(ctx.bot.footer, icon=ctx.bot.get_me().avatar_url)
    await ctx.interaction.create_initial_response(
        ResponseType.MESSAGE_CREATE,
        embed=embed
    )

def load(bot: Bot):
    bot.add_plugin(general_plugin)


def unload(bot: Bot):
    bot.remove_plugin(general_plugin)