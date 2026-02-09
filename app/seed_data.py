from datetime import datetime, timedelta
from .database import SessionLocal, engine, Base
from . import models

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Authors
    authors = [
        models.Author(id=1, name="Priya Sharma", email="priya@example.com"),
        models.Author(id=2, name="Rahul Verma", email="rahul@example.com"),
        models.Author(id=3, name="Anita Desai", email="anita@example.com"),
    ]
    db.add_all(authors)
    db.commit()

    # 2. Books
    books = [
        models.Book(id=1, title="Silent River", author_id=1, royalty_per_sale=100.0),
        models.Book(id=2, title="Midnight in Mumbai", author_id=1, royalty_per_sale=125.0),
        models.Book(id=3, title="Code & Coffee", author_id=2, royalty_per_sale=150.0),
        models.Book(id=4, title="Startup Diaries", author_id=2, royalty_per_sale=175.0),
        models.Book(id=5, title="Poetry of Pain", author_id=3, royalty_per_sale=50.0),
        models.Book(id=6, title="Garden of Words", author_id=3, royalty_per_sale=75.0),
    ]
    db.add_all(books)
    db.commit()

    # 3. Sales to match starting balances
    # Priya = ₹3,825
    # Silent River (100) x 20 = 2000
    # Midnight in Mumbai (125) x 14.6... wait, total must be 3825.
    # 20 * 100 = 2000. 3825 - 2000 = 1825. 1825 / 125 = 14.6 (Not good)
    # Let's try: 17 * 100 = 1700. 3825 - 1700 = 2125. 2125 / 125 = 17. (Perfect!)
    # Priya: 17 sales of Silent River, 17 sales of Midnight in Mumbai.
    
    # Rahul = ₹9,975
    # Code & Coffee (150) x 30 = 4500. 9975 - 4500 = 5475. 5475 / 175 = 31.28
    # Let's try: 32 * 150 = 4800. 9975 - 4800 = 5175. 5175 / 175 = 29.57
    # Let's try: 35 * 150 = 5250. 9975 - 5250 = 4725. 4725 / 175 = 27. (Perfect!)
    # Rahul: 35 sales of Code & Coffee, 27 sales of Startup Diaries.

    # Anita = ₹400
    # Poetry of Pain (50) x 5 = 250. 400 - 250 = 150. 150 / 75 = 2. (Perfect!)
    # Anita: 5 sales of Poetry of Pain, 2 sales of Garden of Words.

    sales = [
        # Priya (Author 1)
        models.Sale(book_id=1, quantity=17, sale_date=datetime.utcnow() - timedelta(days=5)),
        models.Sale(book_id=2, quantity=17, sale_date=datetime.utcnow() - timedelta(days=2)),
        
        # Rahul (Author 2)
        models.Sale(book_id=3, quantity=35, sale_date=datetime.utcnow() - timedelta(days=10)),
        models.Sale(book_id=4, quantity=27, sale_date=datetime.utcnow() - timedelta(days=3)),
        
        # Anita (Author 3)
        models.Sale(book_id=5, quantity=5, sale_date=datetime.utcnow() - timedelta(days=7)),
        models.Sale(book_id=6, quantity=2, sale_date=datetime.utcnow() - timedelta(days=1)),
    ]
    db.add_all(sales)
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
