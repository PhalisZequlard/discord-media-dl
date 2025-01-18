import yt_dlp
import gallery_dl
import asyncio
import os
from typing import Optional, Callable
from config import Config
from .queue_utils import DownloadTask

class DownloadManager:
    @staticmethod
    async def download_video(task: DownloadTask):
        ydl_opts = {
            'format': task.options.get('quality', 'best'),
            'outtmpl': os.path.join(Config.DOWNLOAD_PATH, 'videos', '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: asyncio.create_task(
                task.interaction.edit_original_response(
                    embed=task.create_progress_embed(d['_percent_str'])
                )
            )],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return await asyncio.to_thread(ydl.download, [task.url])
            
    @staticmethod
    async def download_music(task: DownloadTask):
        format_opt = task.options.get('format', 'mp3')
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_opt,
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(Config.DOWNLOAD_PATH, 'music', '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: asyncio.create_task(
                task.interaction.edit_original_response(
                    embed=task.create_progress_embed(d['_percent_str'])
                )
            )],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return await asyncio.to_thread(ydl.download, [task.url])
            
    @staticmethod
    async def download_gallery(task: DownloadTask):
        # Configure gallery-dl options
        options = {
            'directory': os.path.join(Config.DOWNLOAD_PATH, 'gallery'),
            'zip': task.options.get('pack-kind') == 'PDF',
        }
        
        return await asyncio.to_thread(
            gallery_dl.download, [task.url], options
        )