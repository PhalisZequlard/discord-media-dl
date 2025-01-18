import discord
from discord import Embed, ButtonStyle
from typing import Optional
from datetime import datetime

class DownloadEmbed:
    @staticmethod
    def create_download_embed(task):
        embed = Embed(
            title=f"Download: {task.type.value.title()}",
            description=f"URL: {task.url}",
            color=get_status_color(task.status)
        )
        
        embed.add_field(name="Status", value=task.status.value, inline=True)
        if task.progress > 0:
            embed.add_field(name="Progress", value=f"{task.progress:.1f}%", inline=True)
        
        if task.options:
            options_str = "\n".join(f"{k}: {v}" for k, v in task.options.items())
            embed.add_field(name="Options", value=options_str, inline=False)
            
        if task.error:
            embed.add_field(name="Error", value=task.error, inline=False)
            
        if task.started_at:
            embed.set_footer(text=f"Started at {datetime.fromtimestamp(task.started_at).strftime('%Y-%m-%d %H:%M:%S')}")
            
        return embed

def get_status_color(status):
    colors = {
        'processing': discord.Color.blue(),
        'completed': discord.Color.green(),
        'failed': discord.Color.red(),
        'queued': discord.Color.gold(),
        'cancelled': discord.Color.greyple()
    }
    return colors.get(status, discord.Color.default())

# Create button views
class DownloadButtons(discord.ui.View):
    def __init__(self, task):
        super().__init__(timeout=None)
        self.task = task
        
        # Add retry button if failed
        if task.status == 'failed':
            retry_button = discord.ui.Button(
                style=ButtonStyle.primary,
                label="Retry",
                custom_id=f"retry_{task.id}"
            )
            self.add_item(retry_button)
            
        # Add cancel button if not completed/failed
        if task.status not in ['completed', 'failed', 'cancelled']:
            cancel_button = discord.ui.Button(
                style=ButtonStyle.danger,
                label="Cancel",
                custom_id=f"cancel_{task.id}"
            )
            self.add_item(cancel_button)