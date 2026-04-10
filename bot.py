import discord
import re
import requests
import logging
import os
import mysql.connector
import sys
from discord.ext import commands
from mysql.connector import Error
from dotenv import load_dotenv
from colorama import Fore, init, Style
from errors import error_codes

init()

class ColoredFormatter(logging.Formatter):
    """Adds colors to log levels"""
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.BLUE,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, Fore.WHITE)
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s at %(asctime)s : %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stderr)]
)

formatter = ColoredFormatter(
    fmt='%(levelname)s at %(asctime)s : %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger()
for handler in logger.handlers:
    handler.setFormatter(formatter)


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="/", intents=intents, case_insensitive=True)

    async def on_ready(self):
        logging.info(f'{self.user} has connected to Discord!')
        await self.tree.sync()

load_dotenv()

intents = discord.Intents.all()
bot = Bot(intents=intents)
client = discord.Client(intents=intents)

token = os.getenv("token")
status = os.getenv("status")
url_status = "Unknown"
url = "https://oss-auth.thecheese.io/"


def get_error_message(code):
    if str(code) in error_codes:
        return f"{code}: {error_codes[str(code)]}"
    else:
        return f"{code}: Error code not found."


def check_url(uri):
    global url_status
    try:
        response = requests.get(uri, verify=False, timeout=10)
        url_status = ":green_square: Up"
    except requests.exceptions.RequestException:
        url_status = ":red_square: Down"


@bot.hybrid_command(name="status",description="Gets the status of WiiMart")
async def statusy(ctx):
    await ctx.defer()
    check_url(url)
    if status == "Not Set":
        await ctx.send(f"WiiMart Status: {url_status}\nAdmin Status: :person_shrugging: Currently Unset")
    else:
        await ctx.send(f"WiiMart Status: {url_status}\nAdmin Status: {status}")


@bot.hybrid_command(name="setstatus",description="Sets the current server status to your liking")
@commands.has_any_role("Owner", "Admin", "Moderators", "Hoster")
async def setstatus(ctx, stat: str):
    global status
    status = stat
    await ctx.send(f"Status has been set to: {status}")


@bot.hybrid_command(name="unsetstatus", description="Unsets the current status")
@commands.has_any_role("Owner", "Admin", "Moderators", "Hoster")
async def unset(ctx):
    global status
    status = "Not Set"
    await ctx.send("Status has been unset.")


@bot.hybrid_command(name="error", description="Gets the error message linked with the shop error code")
async def geterror(ctx, errorcode: int):
    try:
        errormessage = get_error_message(errorcode)
    except ValueError:
        errormessage = "Error Code was not found."
    await ctx.send(errormessage)


@bot.hybrid_command(name="addfc", description="Adds your Wii Friend code to the list of friend codes so that others can add you")
async def addfc(ctx, fc: int):
    await ctx.defer(ephemeral=True)
    if len(str(fc)) != 16:
        await ctx.send(f"You need to input a friendcode that is of 16 numbers not {len(str(fc))}", ephemeral=True)
    else:
        userid = ctx.author.id
        conn = mysql.connector.connect(host=os.getenv("mqur"), user=os.getenv("mqlu"), password=os.getenv("mqlp"), database=os.getenv("mqld"), port=os.getenv("mqpo"))
        cur = conn.cursor(buffered=True)
        cur.execute(f"SELECT fc FROM usersfc WHERE userid = '{userid}'")
        try:
            fethcy = cur.fetchall()
        except Error as e:
            fetchy = False
        if fethcy:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"UPDATE usersfc SET fc = '{fc}' WHERE userid = '{userid}'")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send("Updated your friend code", ephemeral=True)
        else:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"INSERT INTO usersfc (userid, fc) VALUES ('{userid}', '{fc}')")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send("Added your friend code", ephemeral=True)


@bot.hybrid_command(name="getfc", description="Gets the friend code of the selected user")
async def getfc(ctx, member: discord.Member):
    await ctx.defer(ephemeral=True)
    userid = member.id
    conn = mysql.connector.connect(host=os.getenv("mqur"), user=os.getenv("mqlu"), password=os.getenv("mqlp"), database=os.getenv("mqld"), port=os.getenv("mqpo"))
    cur = conn.cursor(buffered=True)
    cur.execute(f"SELECT fc FROM usersfc WHERE userid = '{userid}'")
    result = cur.fetchone()
    if result and result[0]:
        fetchy = result[0]
        fetchy = " ".join([fetchy[i:i+4] for i in range(0, len(fetchy), 4)])
        await ctx.send(f"<@{userid}> Friend code is: {fetchy}", ephemeral=True)
    else:
        await ctx.send(f"<@{userid}> did not share their friend code.", ephemeral=True)
    cur.close()
    conn.close()


@bot.hybrid_command(name="forceaddfc", description="Force adds the users Wii Friend code to the list of friend codes so that others can add them")
@commands.has_any_role("Owner", "Admin", "Moderators")
async def addfcadm(ctx, user: discord.Member, fc: int):
    await ctx.defer(ephemeral=True)
    if len(str(fc)) != 16:
        userid = user.id
        await ctx.send(f"You need to input a friendcode that is of 16 numbers not {len(str(fc))} for <@{userid}>", ephemeral=True)
    else:
        userid = user.id
        conn = mysql.connector.connect(host=os.getenv("mqur"), user=os.getenv("mqlu"), password=os.getenv("mqlp"), database=os.getenv("mqld"), port=os.getenv("mqpo"))
        cur = conn.cursor(buffered=True)
        cur.execute(f"SELECT fc FROM usersfc WHERE userid = '{userid}'")
        try:
            fethcy = cur.fetchall()
        except Error as e:
            fetchy = False
        if fethcy:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"UPDATE usersfc SET fc = '{fc}' WHERE userid = '{userid}'")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send(f"Updated <@{userid}> friend code", ephemeral=True)
        else:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"INSERT INTO usersfc (userid, fc) VALUES ('{userid}', '{fc}')")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send(f"Added <@{userid}> friend code", ephemeral=True)


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and message.guild:
        try:
            await message.add_reaction('👀')
        except Exception as e:
            logging.error(f'Failed to react to mention: {e}')

    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        try:
            await message.reply("Hey, the staff team can't read this chat! If you have an issue, make a post in <#1458939338468364562> or send an email to us at support@wiimart.org :)")
        except Exception as e:
            logging.error(f'Failed to reply to DM: {e}')

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(token)
