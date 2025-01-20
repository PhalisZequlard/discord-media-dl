from functools import wraps
import asyncio
from discord import Interaction, Embed, Color
from typing import Callable, List
from .db_utils import db_manager

def check_permission():
    """
    Decorator for checking user permissions and active downloads.
    Auto-deletes denial messages after 5 minutes.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            user_id = str(interaction.user.id)
            user_roles = [str(role.id) for role in interaction.user.roles]
            
            try:
                # Check if user is allowed
                is_allowed = await db_manager.is_user_allowed(user_id, user_roles)
                if not is_allowed:
                    # Send permission denied message and delete after 5 minutes
                    embed = Embed(
                        title="Permission Denied",
                        description="Contact the admin to subscribe",
                        color=Color.red()
                    )
                    await interaction.response.send_message(
                        embed=embed,
                        ephemeral=True,
                        delete_after=300  # 5 minutes
                    )
                    return

                # Check for active downloads - silently ignore if user has active download
                has_active = await db_manager.has_active_download(user_id)
                if has_active:
                    # Don't respond, just ignore
                    await interaction.response.defer(ephemeral=True, thinking=False)
                    return

                # If all checks pass, execute the command
                return await func(self, interaction, *args, **kwargs)

            except Exception as e:
                # Log the error and send a generic error message
                print(f"Error in permission check: {e}")
                embed = Embed(
                    title="Error",
                    description="An error occurred while processing your request",
                    color=Color.red()
                )
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        embed=embed,
                        ephemeral=True
                    )
                
    return decorator

async def track_active_download(interaction: Interaction, task_id: str, command_type: str):
    """
    Track an active download for a user.
    Should be called when a download starts.
    """
    user_id = str(interaction.user.id)
    await db_manager.add_active_download(user_id, task_id, command_type)

async def clear_active_download(interaction: Interaction):
    """
    Clear active download tracking for a user.
    Should be called when a download completes or fails.
    """
    user_id = str(interaction.user.id)
    await db_manager.remove_active_download(user_id)