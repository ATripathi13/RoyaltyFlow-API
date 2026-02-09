from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/withdrawals", tags=["withdrawals"])

@router.post("/", response_model=schemas.WithdrawalResponse, status_code=201)
def request_withdrawal(withdrawal: schemas.WithdrawalRequest, db: Session = Depends(get_db)):
    result, status_code = services.create_withdrawal(db, withdrawal.author_id, withdrawal.amount)
    
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result)
    
    return result
