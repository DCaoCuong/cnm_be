from fastapi import Request, HTTPException, status

def require_roles(*roles: str):
    def checker(request: Request):
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        user_role_names = [r.name for r in getattr(user, "roles", [])]
        if not any(role in user_role_names for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )
        return user

    return checker
