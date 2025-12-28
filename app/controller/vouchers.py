from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_pagination, require_roles
from app.schemas.voucher import VoucherCreate, VoucherUpdate, VoucherResponse
from app.schemas.response.base import BaseResponse
from app.controller.voucher_controller import (
    list_vouchers_controller,
    read_voucher_controller,
    create_voucher_controller,
    update_voucher_controller,
    delete_voucher_controller,
)

router = APIRouter(prefix="/vouchers", tags=["vouchers"])

@router.get("/", response_model=BaseResponse[List[VoucherResponse]])
def list_vouchers(params: dict = Depends(get_pagination), db: Session = Depends(get_db)):
    return list_vouchers_controller(db, params)

@router.get("/{voucher_id}", response_model=BaseResponse[VoucherResponse])
def read_voucher(voucher_id: str, db: Session = Depends(get_db)):
    return read_voucher_controller(db, voucher_id)

@router.post("/", response_model=BaseResponse[VoucherResponse], status_code=201)
def create_voucher_endpoint(voucher_in: VoucherCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    return create_voucher_controller(db, voucher_in, current_user)

@router.put("/{voucher_id}", response_model=BaseResponse[VoucherResponse])
def update_voucher_endpoint(voucher_id: str, voucher_in: VoucherUpdate, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    return update_voucher_controller(db, voucher_id, voucher_in, current_user)

@router.delete("/{voucher_id}", response_model=BaseResponse[None])
def delete_voucher_endpoint(voucher_id: str, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    return delete_voucher_controller(db, voucher_id, current_user)
