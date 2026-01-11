# app/core/notification_sockets.py
"""
WebSocket Manager for Notifications - Tách biệt với chat
"""
from fastapi import WebSocket
from typing import Dict
import json


class NotificationConnectionManager:
    def __init__(self):
        # {user_id: websocket_connection}
        self.active_connections: Dict[str, WebSocket] = {}
        # {user_id: role} - track user roles for efficient broadcasting
        self.user_roles: Dict[str, str] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        """Connect a user to notification socket"""
        self.active_connections[user_id] = websocket
        print(f"✅ [NOTIFICATION WS] Connected: {user_id}")
    
    def set_user_role(self, user_id: str, role: str):
        """Track user role for broadcasting purposes"""
        self.user_roles[user_id] = role
        print(f"📋 [NOTIFICATION WS] Set role for {user_id}: {role}")

    def disconnect(self, user_id: str):
        """Disconnect a user from notification socket"""
        if user_id in self.active_connections:
            try:
                ws = self.active_connections[user_id]
                if not ws.client_state.closed:
                    pass
            except Exception:
                pass
            del self.active_connections[user_id]
            print(f"❌ [NOTIFICATION WS] Disconnected: {user_id}")
        
        # Also remove from user_roles
        if user_id in self.user_roles:
            del self.user_roles[user_id]

    async def send_notification(self, user_id: str, notification_data: dict):
        """
        Send notification to a specific user
        notification_data should contain: type, data, unread_count
        """
        ws = self.active_connections.get(user_id)
        if not ws:
            print(f"⚠️ [NOTIFICATION WS] User {user_id} not connected")
            return False
        
        try:
            await ws.send_json(notification_data)
            print(f"✅ [NOTIFICATION WS] Sent to {user_id}: {notification_data.get('type')}")
            return True
        except Exception as e:
            print(f"❌ [NOTIFICATION WS] Error sending to {user_id}: {e}")
            # If send fails (client disconnected), remove connection
            try:
                del self.active_connections[user_id]
                if user_id in self.user_roles:
                    del self.user_roles[user_id]
            except KeyError:
                pass
            return False
    
    async def broadcast_to_admins(self, notification_data: dict):
        """
        Broadcast notification to all connected admin users
        """
        admin_user_ids = [
            user_id for user_id, role in self.user_roles.items() 
            if role == "ADMIN"
        ]
        
        print(f"📢 [NOTIFICATION WS] Broadcasting to {len(admin_user_ids)} admins")
        
        success_count = 0
        for admin_id in admin_user_ids:
            if await self.send_notification(admin_id, notification_data):
                success_count += 1
        
        print(f"✅ [NOTIFICATION WS] Broadcast sent to {success_count}/{len(admin_user_ids)} admins")
        return success_count
    
    async def send_unread_count_update(self, user_id: str, unread_count: int):
        """
        Send unread count update to a specific user
        """
        data = {
            "type": "unread_count_update",
            "data": {
                "unread_count": unread_count
            }
        }
        return await self.send_notification(user_id, data)


# Global instance for notifications
notification_manager = NotificationConnectionManager()
