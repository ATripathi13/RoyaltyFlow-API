from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    royalty_per_sale: float

class BookResponse(BookBase):
    id: int
    total_sold: int
    total_royalty: float

    class Config:
        from_attributes = True

class AuthorBase(BaseModel):
    name: str
    email: Optional[str] = None

class AuthorListResponse(AuthorBase):
    id: int
    total_earnings: float
    current_balance: float

    class Config:
        from_attributes = True

class AuthorDetailResponse(AuthorListResponse):
    total_books: int
    books: List[BookResponse]

    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    book_title: str
    quantity: int
    royalty_earned: float
    sale_date: datetime

    class Config:
        from_attributes = True

class WithdrawalRequest(BaseModel):
    author_id: int
    amount: float

class WithdrawalResponse(BaseModel):
    id: int
    author_id: int
    amount: float
    status: str
    created_at: datetime
    new_balance: float

    class Config:
        from_attributes = True

class WithdrawalHistoryResponse(BaseModel):
    id: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
