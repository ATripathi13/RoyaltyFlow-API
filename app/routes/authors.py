from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/", response_model=List[schemas.AuthorListResponse])
def read_authors(db: Session = Depends(get_db)):
    return services.get_authors(db)

@router.get("/{author_id}", response_model=schemas.AuthorDetailResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author_detail = services.get_author_detail(db, author_id)
    if author_detail is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author_detail

@router.get("/{author_id}/sales", response_model=List[schemas.SaleResponse])
def read_author_sales(author_id: int, db: Session = Depends(get_db)):
    # Check if author exists
    author = services.get_author_detail(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return services.get_author_sales(db, author_id)

@router.get("/{author_id}/withdrawals", response_model=List[schemas.WithdrawalHistoryResponse])
def read_author_withdrawals(author_id: int, db: Session = Depends(get_db)):
    # Check if author exists
    author = services.get_author_detail(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return services.get_author_withdrawals(db, author_id)
