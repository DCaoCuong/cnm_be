from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permission import require_roles
from app.models.user import User
from app.schemas.request.auth import (
    UserCreate, 
    LoginRequest, 
    RefreshTokenRequest, 
    GoogleLoginRequest,
    VerifyEmailRequest,
    ResendVerificationRequest,
    AdminResetPasswordRequest
)
from app.schemas.response.auth import (
    UserResponse, 
    TokenResponse,
    VerifyEmailResponse,
    VerificationStatusResponse,
    RegisterResponse,
    AdminResetPasswordResponse
)
from app.schemas.response.base import BaseResponse
from app.services.auth_service import (
    create_user, 
    authenticate_user, 
    login, 
    renew_tokens, 
    authenticate_google_user,
    admin_reset_password
)
from app.services.email_verification_service import EmailVerificationService

router = APIRouter()

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Đăng ký tài khoản mới.
    
    - Tạo user trong database (email_confirmed=False)
    - Gửi mã xác thực 6 số qua email
    - KHÔNG trả về token
    - User phải verify email trước khi có thể login
    """
    user = create_user(db, user_in, created_by=None)
    
    return RegisterResponse(
        success=True,
        message="Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản.",
        email=user.email,
        verification_sent=True
    )

@router.post("/login", response_model=TokenResponse)
def authentication(form_data: LoginRequest, db: Session = Depends(get_db)):
    # 1. Xác thực user/pass
    print(form_data.password)
    user = authenticate_user(db, form_data.email, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản hoặc mật khẩu không đúng!")
    
    # 2. Tạo token và trả về response kèm thông tin user
    # Logic tạo token + lưu refresh token vào DB đã chuyển vào service
    response_data = login(user, db)
    
    return TokenResponse(**response_data)

@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    API dùng để lấy access token mới bằng refresh token.
    Đồng thời trả về refresh token mới (Rotate Refresh Token).
    """
    token_data = renew_tokens(request.refresh_token, db)
    return TokenResponse(**token_data)

@router.post("/google", response_model=TokenResponse)
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    """
    API xác thực Google OAuth.
    Nhận ID token từ Google, verify và tạo/lấy user, sau đó trả về access token và refresh token.
    """
    # 1. Xác thực Google token và lấy/tạo user
    user = authenticate_google_user(request.id_token, db)
    
    # 2. Tạo token và trả về response (giống flow login thông thường)
    response_data = login(user, db)
    
    return TokenResponse(**response_data)


@router.post("/verify-email", response_model=VerifyEmailResponse)
def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    """
    API xác thực email bằng mã 6 số (PUBLIC - không cần token)
    
    - **email**: Email đã đăng ký
    - **code**: Mã 6 số nhận được qua email
    - Sau khi verify thành công, user có thể login
    """
    service = EmailVerificationService(db)
    success, message = service.verify_email_by_email(request.email, request.code)
    
    return VerifyEmailResponse(
        success=success,
        message=message,
        email_confirmed=True
    )


@router.post("/resend-verification", response_model=BaseResponse[str])
def resend_verification_code(
    request: ResendVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    API gửi lại mã xác thực email (PUBLIC - không cần token)
    
    - **email**: Email đã đăng ký
    - Giới hạn: Tối đa 5 lần gửi lại
    - Cooldown: 60 giây giữa các lần gửi
    """
    service = EmailVerificationService(db)
    success, message = service.send_verification_code_by_email(request.email, is_resend=True)
    
    return BaseResponse(success=success, message=message, data=message)


@router.post("/admin/reset-password", response_model=AdminResetPasswordResponse)
def admin_reset_user_password(
    request: AdminResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: User = Depends(require_roles("ADMIN"))
):
    """
    API cho Admin/Manager reset mật khẩu user.
    
    - **user_id**: ID của user cần reset password
    - Tạo mật khẩu ngẫu nhiên mạnh
    - Gửi email thông báo mật khẩu mới cho user
    - Xóa refresh token (bắt user phải login lại)
    - Chỉ ADMIN hoặc MANAGER mới có quyền sử dụng
    """
    from app.repositories.user_repository import UserRepository
    
    # Kiểm tra user tồn tại và lấy email
    user_repo = UserRepository(db)
    target_user = user_repo.get(request.user_id)
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User không tồn tại"
        )
    
    # Thực hiện reset password
    success, message = admin_reset_password(
        db=db,
        user_id=request.user_id,
        admin_id=str(current_user.id)
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
    
    return AdminResetPasswordResponse(
        success=True,
        message=message,
        email=target_user.email
    )


