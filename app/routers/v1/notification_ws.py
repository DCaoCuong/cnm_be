"""
WebSocket Router for Notifications - Tách biệt với chat
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.core.notification_sockets import notification_manager
from app.repositories.user_repository import UserRepository
from app.services.notification_service import NotificationService

router = APIRouter()


@router.websocket("/ws/notifications")
async def notification_websocket(
    websocket: WebSocket,
    token: str = Query(...),
):
    """
    WebSocket endpoint cho notifications
    Khác với chat, endpoint này chỉ nhận thông báo từ server, không gửi message
    """
    # ✅ 1. PHẢI ACCEPT TRƯỚC
    await websocket.accept()

    # ✅ 2. VERIFY TOKEN
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = payload.get("sub")
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    db: Session = SessionLocal()

    try:
        # ✅ 3. CONNECT MANAGER
        await notification_manager.connect(user_id, websocket)
        print(f"✅ [NOTIFICATION WS] CONNECTED: {user_id}")
        
        # Check if user is admin
        user_repo = UserRepository(db)
        current_user = user_repo.get_with_roles(user_id)
        
        # Determine user role
        user_role = "USER"
        if current_user and current_user.roles:
            is_admin = any(role.name == "ADMIN" for role in current_user.roles)
            if is_admin:
                user_role = "ADMIN"
        
        # Track user role for broadcasting
        notification_manager.set_user_role(user_id, user_role)

        # Send initial unread count
        notification_service = NotificationService(db)
        unread_count = notification_service.get_unread_count(user_id)
        await notification_manager.send_unread_count_update(user_id, unread_count)

        # Keep connection alive and listen for close
        while True:
            # This endpoint only receives heartbeats or close signals
            # Actual notifications are sent from NotificationService
            data = await websocket.receive_json()
            
            # Handle heartbeat/ping messages
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
            # If client sends "get_unread_count", respond immediately
            elif data.get("type") == "get_unread_count":
                unread_count = notification_service.get_unread_count(user_id)
                await notification_manager.send_unread_count_update(user_id, unread_count)

    except WebSocketDisconnect:
        print(f"❌ [NOTIFICATION WS] DISCONNECTED: {user_id}")
        notification_manager.disconnect(user_id)

    except Exception as e:
        print(f"❌ [NOTIFICATION WS] ERROR: {e}")
        notification_manager.disconnect(user_id)

    finally:
        db.close()
