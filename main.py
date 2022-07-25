import logging
import os

from discord.ext import tasks
from izsak import Izsak
from utils import can_upload

logging.basicConfig(level=logging.INFO)
environment = os.environ.get("IZSAK_ENV")
izsak = Izsak()

client = izsak.client


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.slash_command(
    description="meow :3c",
    guild_ids=[izsak.guild_id],
)
async def catgirl(ctx):
    await izsak.send_random_catgirl(ctx)


@client.slash_command(
    description="Retrieve media by category",
    guild_ids=[izsak.guild_id],
)
async def media(ctx, category):
    await izsak.send_media_by_category(ctx, category)


@client.slash_command(
    description="Upload media",
    guild_ids=[izsak.guild_id],
)
async def upload(ctx):
    await Izsak.upload_modal(ctx) if can_upload(ctx) else await Izsak.forbidden(ctx)


@client.slash_command(
    description="Tell Izsak you love him",
    guild_ids=[izsak.guild_id],
)
async def love(ctx):
    await izsak.love(ctx)


@client.slash_command(
    description="What did you just say?",
    guild_ids=[izsak.guild_id],
)
async def wtf(ctx, role):
    await izsak.wtf(ctx, role)


@tasks.loop(hours=12)
async def send_random_catgirl():
    try:
        await izsak.send_random_catgirl()
    except AttributeError as e:
        print(str(e))

if environment == "PROD":
    send_random_catgirl.start()
izsak.start()
