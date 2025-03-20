import discord
from discord.ext import commands
import os
from dotenv import load_dotenv 
import sqlite3
import re
import threading
import requests
import time
import sys


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="!--!--!", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.tree.sync()

load_dotenv()
intents = discord.Intents.all()
bot = Bot(intents=intents)
client = discord.Client(intents=intents)
token = os.getenv("token")
status = os.getenv("status")
url_status = "Unknown"
url = "https://oss-auth.blinklab.com/"
stop_event = threading.Event()

def matches_wildcard(code, wildcard_code):
    pattern = wildcard_code.replace('X', '[0-9]')
    return re.fullmatch(pattern, str(code)) is not None

def get_error_message(code):
    # Connect to the SQLite database
    conn = sqlite3.connect('error_codes.db')
    cursor = conn.cursor()

    # Check for exact matches
    cursor.execute('SELECT message FROM error_codes WHERE code = ?', (str(code),))
    result = cursor.fetchone()

    if result:
        return f"{code}: {result[0]}"

    # Check for wildcard matches
    cursor.execute('SELECT code, message FROM error_codes')
    for row in cursor.fetchall():
        if matches_wildcard(code, row[0]):
            return f"{code}: {row[1]}"

    return f"{code}: Error code not found."

def check_url():
    global url_status  # Declare the global variable to modify it
    try:
        response = requests.get(url, verify=False, timeout=10)  # Disable SSL verification and set a timeout
        url_status = ":green_square: Up"  # If we get a response, set status to "Up"
    except requests.exceptions.RequestException:
        url_status = ":red_square: Down"  # If there's an exception, set status to "Down"

@bot.hybrid_command(name="status",description="Gets the status of WiiMart")
async def statusy(ctx):
    check_url()
    if status == "Not Set":
        await ctx.send(f"WiiMart Status: {url_status}\nAdmin Status: :person_shrugging: Currently Unset")
    else:
        await ctx.send(f"WiiMart Status: {url_status}\nAdmin Status: {status}")

@bot.hybrid_command(name="setstatus",description="Sets the current server status to your liking")
@commands.has_any_role("Owner", "Admin", "Moderators")
async def setstatus(ctx, stat: str):
    global status
    status = stat
    await ctx.send(f"Status has been set to: {status}")

@bot.hybrid_command(name="unsetstatus", description="Unsets the current status")
@commands.has_any_role("Owner", "Admin", "Moderators")
async def unset(ctx):
    global status
    status = "Not Set"
    await ctx.send("Status has been unset.")

@bot.hybrid_command(name="error", description="Gets the error message linked with the shop error code")
async def geterror(ctx, errorcode: commands.Range[int, 204000, 250943]):
    try:
        errormessage = get_error_message(errorcode)
    except ValueError:
        errormessage = "Error Code was not found."
    await ctx.send(errormessage)
    
bot.run(token)