# RoyaltyFlow API

## 🛠 Tech Stack
Built using **FastAPI** and **SQLAlchemy with SQLite** to ensure a high-performance, type-safe, and modular environment suitable for financial backend operations.

## 💰 Assumptions & Business Logic
- **Starting Balances**: Since exact sales data was not provided, I inferred a transaction history that results in the exact starting balances required: Priya (₹3,825), Rahul (₹9,975), and Anita (₹400).
- **Withdrawal Rules**: Enforced a minimum withdrawal threshold of ₹500 and strictly validated requests against the available balance.
- **Production Readiness**: The system uses a service-oriented architecture to keep business logic decoupled from the API layer.

## 🚀 Setup
1. `pip install -r requirements.txt`
2. `python -m app.seed_data` (to initialize database)
3. `uvicorn app.main:app --host 0.0.0.0 --port 8000`
