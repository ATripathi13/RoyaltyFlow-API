# RoyaltyFlow API

A production-ready REST API for managing authors, books, royalties, sales, and withdrawals.

## 🛠 Tech Stack

| Component  | Tech                    |
| ---------- | ----------------------- |
| Framework  | FastAPI                 |
| DB         | SQLite (SQLAlchemy ORM) |
| Validation | Pydantic                |
| CORS       | FastAPI CORSMiddleware  |

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
Seeding the database with initial authors, books, and sales data:
```bash
python -m app.seed_data
```

### 4. Run the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000`. Documentation can be accessed at `http://localhost:8000/docs`.

## 💰 Business Logic & Assumptions

- **Earnings Calculation**: Total earnings are calculated as `sum(book.sales * royalty_per_sale)`.
- **Balance**: Current balance is `total_earnings - total_withdrawals`.
- **Withdrawal Rules**:
    - Minimum ₹500 per request.
    - Cannot exceed the current available balance.
- **Inferred Sales Data**: Since specific sales quantities were not provided in the requirements, I have generated a dataset that results in the following starting balances:
    - **Priya Sharma**: ₹3,825
    - **Rahul Verma**: ₹9,975
    - **Anita Desai**: ₹400

## 🔌 API Endpoints

1. `GET /authors`: List all authors with earnings and balance.
2. `GET /authors/{id}`: Detailed author stats and book list.
3. `GET /authors/{id}/sales`: Sales history for an author (newest first).
4. `GET /authors/{id}/withdrawals`: Withdrawal history for an author (newest first).
5. `POST /withdrawals`: Request a new withdrawal.

## 🚢 Deployment

The app is ready to be deployed on Render or any Python-capable cloud provider using the command:
3. `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## 🚢 Deployment on Render

This project is configured for easy deployment on **Render** via the provided `render.yaml` blueprint.

1. Connect your GitHub repository to Render.
2. Render will automatically detect the `render.yaml` file.
3. The `build.sh` script will install dependencies and seed the database.
4. Alternatively, use these settings for a manual Web Service:
   - **Environment**: `Python`
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
