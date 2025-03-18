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

bot.run(token)