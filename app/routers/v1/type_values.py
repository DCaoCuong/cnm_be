from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.pagination import get_pagination
from app.dependencies.permission import require_roles
from app.schemas.request.type import (
    TypeValueCreate,
    TypeValueUpdate,
    TypeValueResponse,
)
from app.schemas.response.base import BaseResponse
from app.services.type_service import (
    list_type_values,
    create_type_value,
    update_type_value,
    delete_type_value,
    get_type_value,
)

router = APIRouter(prefix="/{type_id}/values", tags=["type-values"])


@router.get("/", response_model=BaseResponse[List[TypeValueResponse]])
def list_values(type_id: str, params: dict = Depends(get_pagination), db: Session = Depends(get_db), current_user = Depends(require_roles("CLIENT", "ADMIN"))):
    items, total = list_type_values(db, type_id, skip=params.get("skip", 0), limit=params.get("limit", 100))
    meta = {**params, "total": total}
    return BaseResponse(success=True, message="OK", data=items, meta=meta)


@router.post("/", response_model=BaseResponse[TypeValueResponse], status_code=status.HTTP_201_CREATED)
def create_value(type_id: str, value_in: TypeValueCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    try:
        obj = create_type_value(db, type_id, value_in, created_by=str(current_user.id) if current_user else None)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent type not found")
    return BaseResponse(success=True, message="Created", data=obj)


@router.get("/{value_id}", response_model=BaseResponse[TypeValueResponse])
def read_value(type_id: str, value_id: str, db: Session = Depends(get_db), current_user = Depends(require_roles("CLIENT", "ADMIN"))):
    obj = get_type_value(db, value_id)
    if not obj or obj.type_id != type_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Value not found")
    return BaseResponse(success=True, message="OK", data=obj)


@router.put("/{value_id}", response_model=BaseResponse[TypeValueResponse])
def update_value(type_id: str, value_id: str, value_in: TypeValueUpdate, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    obj = update_type_value(db, value_id, value_in, updated_by=str(current_user.id) if current_user else None)
    if not obj or obj.type_id != type_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Value not found")
    return BaseResponse(success=True, message="Updated", data=obj)


@router.delete("/{value_id}", response_model=BaseResponse[None])
def delete_value(type_id: str, value_id: str, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    obj = get_type_value(db, value_id)
    if not obj or obj.type_id != type_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Value not found")
    ok = delete_type_value(db, value_id, deleted_by=str(current_user.id) if current_user else None)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Value not found")
    return BaseResponse(success=True, message="Deleted", data=None)
