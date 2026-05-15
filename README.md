# Expense Tracker

A web application for personal expense analysis. Users can register, manage financial tables, add transactions in different currencies (UAH/USD/EUR), and see total expenses converted to hryvnia at current exchange rates.

This project was developed as part of pre-graduation practice.

## Features

- Registration and authentication via email (without using a username field)
- Multiple financial tables per user (for example: "Personal", "Work")
- CRUD operations for transactions: amount, currency, date, categories, description
- Search, filtering (by category, date range), sorting (by date or by amount with currency conversion)
- Currency conversion to UAH via [Open Exchange Rates API](https://openexchangerates.org)
- Analytics page with a doughnut chart showing expense distribution by category
- Client-side password validation with live feedback
- Data protection: users can only access their own tables and transactions
- Admin panel with search, filters, and sorting
- Default categories (Groceries, Auto, Clothing, etc.) are automatically created via data migration

## Tech Stack

- **Backend**: Python 3.12, Django 6.0
- **Database**: SQLite (for dev environment)
- **Frontend**: Django Templates, Bootstrap 5, Chart.js, vanilla JavaScript
- **External API**: Open Exchange Rates (currency rates)
- **Code quality**: flake8, isort

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/expense-tracker.git
cd expense-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activation:

- **Windows**: `venv\Scripts\activate`
- **MacOS / Linux**: `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root, following the `.env.example` template:

```
OPENEXCHANGERATES_APP_ID=your_api_key_here
```

You can get a free API key at [openexchangerates.org/signup/free](https://openexchangerates.org/signup/free) (1000 requests per month).

Without the key the app will still start, but currency conversion and analytics features will not work.

### 5. Apply migrations

```bash
python manage.py migrate
```

Default categories (Groceries, Auto, Clothing, etc.) are added automatically via data migration.

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`

## Linters

Check the code:

```bash
flake8 .
isort --check-only .
```

Automatically format imports:

```bash
isort .
```

Configuration:
- `.flake8` — `max-line-length=120`, migrations and venv are excluded
- `pyproject.toml` — `profile=black`, `line_length=120`, custom import sections (stdlib → django → third-party → first-party)

## Screenshots
