from discord import app_commands, Interaction
from discord.ext import commands
import discord
import uuid
from utils.queue_utils import DownloadTask, DownloadType, DownloadStatus, download_queue
from utils.embed_utils import DownloadEmbed, DownloadButtons
from utils.permission_utils import check_permission, track_active_download

class MusicDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="download-music", description="Download music from supported platforms")
    @check_permission()
    async def download_music(self, interaction: Interaction, url: str):
        # Create format selection buttons
        view = discord.ui.View()
        
        for format_type in ["MP3", "M4A", "Original"]:
            button = discord.ui.Button(
                label=format_type,
                style=discord.ButtonStyle.primary,
                custom_id=f"format_{format_type.lower()}"
            )
            view.add_item(button)
            
        view.add_item(discord.ui.Button(
            label="Cancel",
            style=discord.ButtonStyle.danger,
            custom_id="cancel"
        ))

        # Send initial message
        await interaction.response.send_message(
            embed=discord.Embed(title="Music Download", description="Please select format:"),
            view=view
        )

        try:
            # Wait for button interaction
            interaction_response = await self.bot.wait_for(
                "interaction",
                timeout=60.0,
                check=lambda i: i.user.id == interaction.user.id and i.message.id == interaction.original_response().id
            )

            if interaction_response.data["custom_id"] == "cancel":
                await interaction.edit_original_response(
                    embed=discord.Embed(title="Download Cancelled", color=discord.Color.red()),
                    view=None
                )
                return

            # Get selected format
            selected_format = interaction_response.data["custom_id"].split("_")[1]

            # Create download task
            task = DownloadTask(
                id=str(uuid.uuid4()),
                url=url,
                type=DownloadType.MUSIC,
                interaction=interaction,
                status=DownloadStatus.QUEUED,
                options={"format": selected_format}
            )

            # Track active download
            await track_active_download(interaction, task.id, "music")
            
            # Add to queue
            await download_queue.add_task(task)

            # Update message with initial status
            await interaction.edit_original_response(
                embed=DownloadEmbed.create_download_embed(task),
                view=DownloadButtons(task)
            )

        except TimeoutError:
            await interaction.edit_original_response(
                embed=discord.Embed(title="Selection timed out", color=discord.Color.red()),
                view=None
            )

async def setup(bot):
    await bot.add_cog(MusicDownloader(bot))