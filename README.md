# Flask Transaction Manager

A simple and elegant web application built with Flask, Flask-WTF, and Flask-SQLAlchemy to manage users, transactions, and statistics. Includes a dashboard, admin panel, and RESTful API with Swagger documentation.

---

## Features

- Dashboard
  - View statistics like:
    - Total users
    - Total transactions
    - Total transaction amounts for the day
  - See the latest transactions.
  
- Users Management
  - Add, edit, and delete users.
  - Assign roles: Admin or User.
  
- Transactions Management
  - List, view, and update transaction statuses.
  - Change transaction status (e.g., Confirmed, Canceled).
  
- API
  - /create_transaction - Create a transaction (with automatic commission calculation).
  - /cancel_transaction - Cancel a transaction.
  - /check_transaction - Get transaction status.
  - /swagger - documentation.
  
- Background Tasks
  - Expire transactions after 15 minutes using Celery.
  - Send webhooks on transaction expiration.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sarafantofun/FlaskTransactionManager.git
cd FlaskTransactionManager
```

### 2. Install dependencies using Poetry:
```bash
poetry install
```

### 3. Initialize the Database
```bash
flask db init
flask db migrate
flask db upgrade
```
### 4. Create an Admin User
```bash
flask create-admin
```
### 5. Run the Server
```bash
flask run
```
### 6. Start Celery Worker в новом терминале!
```bash
celery -A tasks worker --loglevel=info
```

## API Endpoints

1. Create Transaction
POST /create_transaction

{
  "user_id": 1,
  "amount": 100.0
}
2. Cancel Transaction
POST /cancel_transaction

{
  "transaction_id": 1
}
3. Check Transaction Status
GET /check_transaction?transaction_id=1

## Admin Panel

The admin panel includes:

Dashboard: View statistics and recent transactions.
Users: Manage users (add, edit, delete).
Transactions: Manage transactions (filter, change status).
Background Tasks

Expire Transactions: Transactions with the status "waiting" expire after 15 minutes.
Status changes to "expired."
A webhook is sent to the user's URL.
Optional Task: Periodically check USDT wallet balances (for advanced users).
Additional Features

Auto-refresh in admin panel (configurable: 0, 10, 15, 30 seconds, or 1 minute).
Filter transactions by:
User
Status (waiting, confirmed, canceled, expired).
Role-based access:
Admin: Full access.
User: View only their own transactions.
Screenshots

## Dashboard
<img src="screenshots/dashboard.png" alt="Dashboard" width="100%">
Users Management
<img src="screenshots/users.png" alt="Users" width="100%">
Transactions Management
<img src="screenshots/transactions.png" alt="Transactions" width="100%">

## License

This project is licensed under the MIT License. 

## Author

Created by Tanya Sarafanova.