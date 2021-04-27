import discord
from discord.ext import commands
import db
import config


def get_prefix(bot, msg):
    prefix = commands.when_mentioned_or('!')(bot, msg)
    try:
        prefix = commands.when_mentioned_or(db.get_prefix(msg.guild))(bot, msg)
    except AttributeError:
        prefix = commands.when_mentioned_or('!')(bot, msg)
    finally:
        return prefix


client = commands.AutoShardedBot(
    command_prefix=get_prefix,
    case_insensitive=True,
    description="بوت فذكروني",
    Intents=discord.Intents.default(),
    shard_count=5
)


client.remove_command("help")

cogs = [
    "prefix",
    "help",
    "commands",
    "setroom",
    "set_time",
    "play",
    'errors',
    # 'test',
    'event',
    'set',
    'owner'
]

for i in cogs:
    try:
        client.load_extension(f"cogs.{i}")
        print(f"load: {i}")
    except Exception as error:
        print(f"the error is \n{error}")

client.load_extension("tasks.send")

client.owner_ids = config.owners


# @tasks.loop(seconds=5.0)
# async def status():
#     status = [
#         '!help - فاذكروني',
#         'رمضان كريم',
#         random.choice(config.all)
#     ]
#     await client.change_presence(activity=discord.Game(type=discord.ActivityType.listening, name=status[0]),
#                                  status=discord.Status.idle)
#     await asyncio.sleep(30)
#     await client.change_presence(activity=discord.Game(type=discord.ActivityType.watching, name=status[1]),
#                                  status=discord.Status.idle)
#     await asyncio.sleep(10)
#     await client.change_presence(activity=discord.Game(type=discord.ActivityType.playing, name=status[2]),
#                                  status=discord.Status.idle)
#     await asyncio.sleep(10)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(type=discord.ActivityType.listening, name='!help - رمضان كريم 🌙'),
                                 status=discord.Status.idle)
    print(f"Name: {client.user.name}\nID: {client.user.id}")


@client.event
async def on_shard_ready(shard_id):
    print(f'`shard {shard_id} is ready`')


client.run(config.token)
