from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict
import asyncio
from datetime import datetime
from config import Config

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self._connection_lock = asyncio.Lock()
        
    async def connect(self):
        """Connect to MongoDB if not already connected"""
        if self.client is None:
            async with self._connection_lock:
                if self.client is None:  # Double-check pattern
                    self.client = AsyncIOMotorClient(Config.MONGODB_URI)
                    self.db = self.client[Config.MONGODB_DB_NAME]
                    
                    # Ensure indexes exist
                    await self._create_indexes()

    async def _create_indexes(self):
        """Create necessary indexes if they don't exist"""
        # Allowed Users indexes
        await self.db.allowed_users.create_index("user_id", unique=True)
        await self.db.allowed_users.create_index([("nickname", "text")])
        await self.db.allowed_users.create_index("active")

        # Allowed Roles indexes
        await self.db.allowed_roles.create_index("role_id", unique=True)
        await self.db.allowed_roles.create_index([("name", "text")])
        await self.db.allowed_roles.create_index("active")

        # Active Downloads indexes
        await self.db.active_downloads.create_index("user_id", unique=True)
        await self.db.active_downloads.create_index(
            "started_at", 
            expireAfterSeconds=3600  # Auto-delete after 1 hour
        )
        await self.db.active_downloads.create_index("task_id")

    # Permission Management Methods
    async def add_allowed_user(self, user_id: str, nickname: str) -> bool:
        """Add a user to allowed users"""
        await self.connect()
        try:
            await self.db.allowed_users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "nickname": nickname,
                        "active": True
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error adding allowed user: {e}")
            return False

    async def remove_allowed_user(self, user_id: str) -> bool:
        """Remove a user from allowed users"""
        await self.connect()
        try:
            result = await self.db.allowed_users.delete_one({"user_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error removing allowed user: {e}")
            return False

    async def add_allowed_role(self, role_id: str, name: str) -> bool:
        """Add a role to allowed roles"""
        await self.connect()
        try:
            await self.db.allowed_roles.update_one(
                {"role_id": role_id},
                {
                    "$set": {
                        "role_id": role_id,
                        "name": name,
                        "active": True
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error adding allowed role: {e}")
            return False

    async def remove_allowed_role(self, role_id: str) -> bool:
        """Remove a role from allowed roles"""
        await self.connect()
        try:
            result = await self.db.allowed_roles.delete_one({"role_id": role_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error removing allowed role: {e}")
            return False

    async def is_user_allowed(self, user_id: str, user_roles: List[str]) -> bool:
        """Check if user is allowed based on their ID or roles"""
        await self.connect()
        try:
            # Check if user ID is directly allowed
            user_allowed = await self.db.allowed_users.find_one(
                {"user_id": user_id, "active": True}
            )
            if user_allowed:
                return True

            # Check if any of user's roles are allowed
            if user_roles:
                role_allowed = await self.db.allowed_roles.find_one(
                    {"role_id": {"$in": user_roles}, "active": True}
                )
                return bool(role_allowed)

            return False
        except Exception as e:
            print(f"Error checking user permissions: {e}")
            return False

    # Active Downloads Management Methods
    async def add_active_download(self, user_id: str, task_id: str, command_type: str) -> bool:
        """Add an active download for a user"""
        await self.connect()
        try:
            await self.db.active_downloads.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "task_id": task_id,
                        "command_type": command_type,
                        "started_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error adding active download: {e}")
            return False

    async def remove_active_download(self, user_id: str) -> bool:
        """Remove an active download for a user"""
        await self.connect()
        try:
            result = await self.db.active_downloads.delete_one({"user_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error removing active download: {e}")
            return False

    async def has_active_download(self, user_id: str) -> bool:
        """Check if user has an active download"""
        await self.connect()
        try:
            active_download = await self.db.active_downloads.find_one({"user_id": user_id})
            return bool(active_download)
        except Exception as e:
            print(f"Error checking active download: {e}")
            return False

    async def search_allowed_users(self, query: str) -> List[Dict]:
        """Search allowed users by nickname"""
        await self.connect()
        try:
            cursor = self.db.allowed_users.find(
                {"$text": {"$search": query}},
                {"score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})])
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error searching allowed users: {e}")
            return []

    async def search_allowed_roles(self, query: str) -> List[Dict]:
        """Search allowed roles by name"""
        await self.connect()
        try:
            cursor = self.db.allowed_roles.find(
                {"$text": {"$search": query}},
                {"score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})])
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error searching allowed roles: {e}")
            return []

# Create global database manager instance
db_manager = DatabaseManager()