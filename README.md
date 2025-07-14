# alx-backend-python
# Database Seeder — `seed.py`

This script sets up a MySQL database called `ALX_prodev`, creates a `user_data` table, and populates it with sample data from a CSV file.

---

## Features

- Connects to a MySQL server
- Creates the `ALX_prodev` database if it doesn't exist
- Creates the `user_data` table with the following schema:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table from `user_data.csv` (skipping duplicate emails)

---

## Requirements

- Python 3.8+
- MySQL Server
- `mysql-connector-python`
- `python-dotenv` (optional for environment variables)

---

