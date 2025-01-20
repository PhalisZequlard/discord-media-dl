import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from config import Config
from web.server import start_web_server
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DownloaderBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",  # We won't use this but it's required
            intents=discord.Intents.default(),
            application_id=Config.APPLICATION_ID
        )
        
    async def setup_hook(self):
        # Load cogs
        for cog in ['video', 'music', 'gallery']:
            await self.load_extension(f'cogs.{cog}')
        
        # Sync commands
        await self.tree.sync()

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

async def main():
    # Start the bot
    bot = DownloaderBot()
    
    # Start web server in the background
    asyncio.create_task(start_web_server())
    
    # Start the bot
    await bot.start(Config.BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())