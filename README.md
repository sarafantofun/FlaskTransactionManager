# Flask Transaction Manager

A simple and elegant web application built with Flask, Flask-WTF, and Flask-SQLAlchemy to manage users, transactions, and statistics. Includes a dashboard, admin panel, and RESTful API with Swagger documentation.

---

## Technologies Used

This project utilizes the following technologies:
- **Flask** for the web framework.
- **SQLAlchemy** for database interactions.
- **Celery** for handling asynchronous background tasks that support various operations within the application.

## Features

This application provides a powerful admin panel for comprehensive management of users and transactions, along with detailed statistical insights. Additionally, it offers:
 
- **API**:
  - /swagger: Access to API documentation.
  - /create_transaction: Endpoint to create a transaction, includes automatic commission calculation.
  - /cancel_transaction: Endpoint to cancel an existing transaction.
  - /check_transaction: Endpoint to check the status of a transaction.  
  
- **Background Tasks**:
  - Expire transactions after 15 minutes using Celery: Automatically changes the status of transactions to 'Expired' if not confirmed within 15 minutes.
  - Send webhooks on transaction expiration: Notifies external systems or components when a transaction status changes to 'Expired'.

For full details on administrative functionalities, refer to the Admin Panel section.

---

## Setup Instructions

1. Redis Configuration. This project requires Redis to function properly. Follow the appropriate section below based on your current Redis setup:
  - If Redis is already installed:
     - Ensure that Redis is running and accessible on port 6379. This is the default port for Redis, and it should be open for connections.
  - If Redis is not installed:
    - Ensure Docker Desktop is installed on your system. If not, [download Docker Desktop from the official Docker website](https://docs.docker.com/desktop/).
    - Open your terminal and execute the following command to start Redis using Docker:
    ```bash
    docker run --name my-redis -p 6379:6379 -d redis
    ```
    This command will start Redis in a Docker container, making it accessible on port 6379 of your local machine. Make sure this port is not being used by any other applications before running this command.

2. Clone the Repository
```bash
git clone https://github.com/sarafantofun/FlaskTransactionManager.git
cd FlaskTransactionManager
```

3. Install dependencies using Poetry:
```bash
poetry install
```
4. Activate the Virtual Environment After installing dependencies, activate the virtual environment created by Poetry:
```bash
poetry shell
```

5. Initialize the Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Create an Admin User
```bash
flask create-admin
```

7. Run the Server
```bash
flask run
```

8. Start Celery Worker in a separate terminal window
```bash
celery -A tasks worker --loglevel=info
```

## API Endpoints

- **Create Transaction**
  **POST** `/create_transaction`
  - Creates a new transaction with the given details.
  **Body:**
    ```json
    {
    "user_id": 1, 
    "amount": 100.0
    }
    ```
  - Response: JSON with the created transaction details.


- **Cancel Transaction**
  **POST** `/cancel_transaction`
  - Cancels a transaction by its ID.
  **Body:**
    ```json
    {
      "transaction_id": 5
    }
    ```


- **Check Transaction Status**
  **GET** `/check_transaction?transaction_id=1`
  - Checks the status of a transaction using its ID.

## Admin Panel

The admin panel is accessible via the `/admin` route and includes the following features:

- **Dashboard**:
  - View statistics like:
    - Total users: Displays the number of registered users.
    - Total transactions: Shows the number of transactions processed.
    - Total transaction amounts for the day: Summarizes the total amount of transactions made within the current day.
  - See the latest transactions: Displays the most recent transactions processed by the system.
  
- **Users Management**:
  - Add, edit, and delete user profiles.
  - Assign roles: Admin or User, determining access levels within the application.
  
- **Transactions Management**:
  - List, view, and manually update transaction statuses.
  - Change transaction status (e.g., Confirmed, Canceled): Allows administrators to update the status as needed.

## License

This project is licensed under the MIT License. 

## Author

Created by Tanya Sarafanova.
