from discord import app_commands, Interaction, SelectOption
from discord.ext import commands
import discord
import uuid
from utils.queue_utils import DownloadTask, DownloadType, DownloadStatus, download_queue
from utils.embed_utils import DownloadEmbed, DownloadButtons
from utils.permission_utils import check_permission, track_active_download

class VideoDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="download-video", description="Download a video from supported platforms")
    @check_permission()
    async def download_video(self, interaction: Interaction, url: str):
        # Create quality selection dropdown
        quality_select = discord.ui.Select(
            placeholder="Select video quality",
            options=[
                SelectOption(label="Best", value="best", default=True),
                SelectOption(label="720p", value="720"),
                SelectOption(label="480p", value="480")
            ],
            custom_id="quality_select"
        )

        # Create view with quality selection and cancel button
        view = discord.ui.View()
        view.add_item(quality_select)
        view.add_item(discord.ui.Button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="cancel"))

        # Send initial message
        await interaction.response.send_message(
            embed=discord.Embed(title="Video Download", description="Please select video quality:"),
            view=view
        )

        try:
            # Wait for interaction with the dropdown or button
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

            # Get selected quality
            selected_quality = interaction_response.data["values"][0]

            # Create download task
            task = DownloadTask(
                id=str(uuid.uuid4()),
                url=url,
                type=DownloadType.VIDEO,
                interaction=interaction,
                status=DownloadStatus.QUEUED,
                options={"quality": selected_quality}
            )

            # Track active download
            await track_active_download(interaction, task.id, "video")
            
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
    await bot.add_cog(VideoDownloader(bot))