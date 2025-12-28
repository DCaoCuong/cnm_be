from core.exceptions.base import BusinessException
from typing import String

class UserNotFoundException(BusinessException):
    def __init__ (self, user_id = String):
         super().__init__(
            message=f"Student {student_id} not found",
            error_code="USER_NOT_FOUND",
            status_code=404,
            extra={"student_id": user_id},
        )
class UserEmailAlreadyExistsException(BusinessException):
    def __init__(self, email: str):
        super().__init__(
            message="Email already exists",
            error_code="EMAIL_ALREADY_EXISTS",
            status_code=409,
            extra={"email": email},
        )
