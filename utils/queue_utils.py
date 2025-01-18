from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, Any
import asyncio
import time
from discord import Interaction, Embed

class DownloadType(Enum):
    VIDEO = "video"
    MUSIC = "music"
    GALLERY = "gallery"

class DownloadStatus(Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class DownloadTask:
    id: str  # Unique task ID
    url: str
    type: DownloadType
    interaction: Interaction
    status: DownloadStatus
    progress: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    options: dict = None
    error: Optional[str] = None

class DownloadQueue:
    def __init__(self, max_concurrent: int = 3):
        self.queue = asyncio.PriorityQueue()
        self.active_downloads = {}
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    async def add_task(self, task: DownloadTask, priority: int = 1):
        await self.queue.put((priority, task))
        await self._update_embed(task)
        
    async def cancel_task(self, task_id: str):
        if task_id in self.active_downloads:
            task = self.active_downloads[task_id]
            task.status = DownloadStatus.CANCELLED
            await self._update_embed(task)
            del self.active_downloads[task_id]
            
    async def process_queue(self):
        while True:
            try:
                async with self.semaphore:
                    priority, task = await self.queue.get()
                    self.active_downloads[task.id] = task
                    task.status = DownloadStatus.PROCESSING
                    task.started_at = time.time()
                    await self._update_embed(task)
                    
                    try:
                        # Process download based on type
                        if task.type == DownloadType.VIDEO:
                            await self._process_video(task)
                        elif task.type == DownloadType.MUSIC:
                            await self._process_music(task)
                        elif task.type == DownloadType.GALLERY:
                            await self._process_gallery(task)
                            
                        task.status = DownloadStatus.COMPLETED
                    except Exception as e:
                        task.status = DownloadStatus.FAILED
                        task.error = str(e)
                    
                    task.completed_at = time.time()
                    await self._update_embed(task)
                    del self.active_downloads[task.id]
                    self.queue.task_done()
                    
            except Exception as e:
                print(f"Queue processing error: {e}")
                await asyncio.sleep(1)
                
    async def _update_embed(self, task: DownloadTask):
        embed = Embed(
            title=f"Download Status: {task.type.value}",
            description=f"URL: {task.url}\nStatus: {task.status.value}"
        )
        
        if task.progress > 0:
            embed.add_field(
                name="Progress",
                value=f"{task.progress:.1f}%",
                inline=True
            )
            
        if task.error:
            embed.add_field(
                name="Error",
                value=task.error,
                inline=False
            )
            
        await task.interaction.edit_original_response(embed=embed)

# Initialize global queue
download_queue = DownloadQueue(max_concurrent=3)