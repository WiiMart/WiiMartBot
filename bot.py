import discord
from discord.ext import commands
import os
from dotenv import load_dotenv 

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

@bot.hybrid_command(name="status",description="Gets the status of WiiMart")
async def statusy(ctx):
    if status == "Not Set":
        await ctx.send("The status hasnt been set by an admin yet, please check again later.")
    else:
        await ctx.send(f"The Current status is: {status}")

@bot.hybrid_command(name="setstatus",description="Sets the current server status to your liking")
@commands.has_any_role("Owner", "Admin", "Moderators")
async def setstatus(ctx, stat: str):
    global status
    status = stat
    await ctx.send(f"Status has been set to: {status}")
    

bot.run(token)