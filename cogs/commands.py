import discord
from discord import Embed, Colour
from discord.ext import commands
import time
import db


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping", help='ارسال سرعة اتصال البوت')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def ping_command(self, ctx):
        before = time.monotonic()
        msg = await ctx.send('pong!!!')
        ping = (time.monotonic() - before) * 1000
        embed = Embed(
            description="`-` Time taken: **{}ms** <a:ping:845021892943544330>\n`-` Discord API: **{}ms** <a:ping:845021892943544330>".format(
            int(ping),
            round(self.client.latency * 1000)
			),color=0xEFD881
        )
        embed.set_author(name=" فاذكروني", icon_url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await msg.edit(content="pong!! <a:discord:846498253674643478>", embed=embed)

    @commands.command(name="support", aliases=['server', "inv", "invite"], help="سيرفر الدعم الفني")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def support_command(self, ctx):
        embed = Embed(
            title='شكرا على اختيارك بوت فاذكروني 🌹',
            description="""
<:111:846484560120250389><:115:846484554126196766><:112:846484559645638697><:113:846484558235828255><:114:846484555782684742><:115:846484554126196766><:116:846484554213752872>
**Link:**
[click here](https://discord.com/oauth2/authorize?client_id=728782652454469662&permissions=8&scope=bot)
**Support:**
[click here](https://discord.gg/MYEvygbHXt)
**Vote:**
[click here](https://top.gg/bot/728782652454469662/vote)
**Support us:**
[click here](https://www.paypal.com/paypalme/codexv) 

<:001:846485195884593263><:005:846485185271824495><:002:846485195016110100><:003:846485193380462662><:004:846485186476900402><:005:846485185271824495><:006:846485183070339072>
""",
            color=0xEFD881)
        # embed.set_image(url="https://i8.ae/djPWO")
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text="بطلب من: {}".format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="info", aliases=['معلومات'], help="الحصول على معلومات الخادم المحفوضه")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def info_(self, ctx):
        data = db.get_info(ctx.guild)
        embed = discord.Embed(
            description='إعدادات خادم: {}'.format(ctx.guild.name),
            color=0xEFD881
        )
        embed.add_field(name='البادئه:', value=data[2], inline=True)
        embed.add_field(name='روم الاذكار:', value=self.client.get_channel(data[3]).mention if data[3] is not None else "لا يوجد", inline=True)
        embed.add_field(name='وقت ارسال الاذكار:', value=str(data[4]), inline=True)
        embed.add_field(name='وضع تكرار الرسائل:', value="<:on:843739804973531176>" if data[5] == 1 else "<:off:843739805309468674>", inline=True)
        embed.add_field(name='وضع الامبد:', value="<:on:843739804973531176>" if data[6] == 1 else "<:off:843739805309468674>", inline=True)
        embed.add_field(name='shard id:', value=str(ctx.guild.shard_id), inline=True)
        embed.add_field(name='shard ping:', value=f"{int(self.client.get_shard(ctx.guild.shard_id).latency * 1000)}ms<a:ping:845021892943544330>", inline=True)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
