from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from datetime import datetime

def get_author_earnings_info(db: Session, author_id: int):
    # Sum of (sale qty * book royalty_per_sale)
    total_earnings = db.query(func.sum(models.Sale.quantity * models.Book.royalty_per_sale))\
        .join(models.Book)\
        .filter(models.Book.author_id == author_id).scalar() or 0.0
    
    # Sum of withdrawals
    total_withdrawals = db.query(func.sum(models.Withdrawal.amount))\
        .filter(models.Withdrawal.author_id == author_id).scalar() or 0.0
    
    current_balance = total_earnings - total_withdrawals
    return total_earnings, current_balance

def get_authors(db: Session):
    authors = db.query(models.Author).all()
    result = []
    for author in authors:
        earnings, balance = get_author_earnings_info(db, author.id)
        result.append({
            "id": author.id,
            "name": author.name,
            "total_earnings": earnings,
            "current_balance": balance
        })
    return result

def get_author_detail(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        return None
    
    total_earnings, current_balance = get_author_earnings_info(db, author_id)
    
    books_data = []
    for book in author.books:
        total_sold = db.query(func.sum(models.Sale.quantity))\
            .filter(models.Sale.book_id == book.id).scalar() or 0
        total_royalty = total_sold * book.royalty_per_sale
        books_data.append({
            "id": book.id,
            "title": book.title,
            "royalty_per_sale": book.royalty_per_sale,
            "total_sold": total_sold,
            "total_royalty": total_royalty
        })
    
    return {
        "id": author.id,
        "name": author.name,
        "email": author.email,
        "current_balance": current_balance,
        "total_earnings": total_earnings,
        "total_books": len(author.books),
        "books": books_data
    }

def get_author_sales(db: Session, author_id: int):
    sales = db.query(models.Sale)\
        .join(models.Book)\
        .filter(models.Book.author_id == author_id)\
        .order_by(models.Sale.sale_date.desc()).all()
    
    result = []
    for sale in sales:
        result.append({
            "book_title": sale.book.title,
            "quantity": sale.quantity,
            "royalty_earned": sale.quantity * sale.book.royalty_per_sale,
            "sale_date": sale.sale_date
        })
    return result

def create_withdrawal(db: Session, author_id: int, amount: float):
    if amount < 500:
        return "Minimum ₹500 required", 400
    
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        return "Author not found", 404
    
    _, current_balance = get_author_earnings_info(db, author_id)
    if amount > current_balance:
        return "Cannot exceed balance", 400
    
    new_withdrawal = models.Withdrawal(
        author_id=author_id,
        amount=amount,
        status="pending",
        created_at=datetime.utcnow()
    )
    db.add(new_withdrawal)
    db.commit()
    db.refresh(new_withdrawal)
    
    _, updated_balance = get_author_earnings_info(db, author_id)
    
    return {
        "id": new_withdrawal.id,
        "author_id": new_withdrawal.author_id,
        "amount": new_withdrawal.amount,
        "status": new_withdrawal.status,
        "created_at": new_withdrawal.created_at,
        "new_balance": updated_balance
    }, 201

def get_author_withdrawals(db: Session, author_id: int):
    return db.query(models.Withdrawal)\
        .filter(models.Withdrawal.author_id == author_id)\
        .order_by(models.Withdrawal.created_at.desc()).all()
