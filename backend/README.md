# Backend

## Setup Instructions

### 1. Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Copy and Edit `.env`
```bash
cp .env.example .env
```

Set your values in .env

### 4. Set Up PostgreSQL
```bash
sudo service postgresql start
sudo -u postgres createdb yourdb
sudo -u postgres psql
# Then in psql:
ALTER USER postgres WITH PASSWORD 'changeme123';
\q
```

### 5. Initialize and Run Migrations
```bash
flask db init
flask db migrate -m "initial schema"
flask db upgrade

```

### 6. Run the Server
```bash
flask run
```

---

## Database Storage Behavior

### Scenario 1: Using PostgreSQL
```env
DATABASE_URL=postgresql://postgres:changeme123@localhost/yourdb
```
In this case, the database is managed by PostgreSQL, not stored in your project folder.

- Your data lives in PostgreSQL’s data directory (usually `/var/lib/postgresql/…`)
- The `instance/` folder is **not used** for storing the DB in this case

---

### Scenario 2: Using SQLite
```env
DATABASE_URL=sqlite:///instance/myapp.db
```
In this case:

- The file will be stored **inside your `instance/` folder**
- You will see `myapp.db` appear there after tables are created

---

## Redis Configuration (Optional)

The `config/redis.conf` file is provided for advanced usage, in case you want to start a custom Redis server manually.

Most users will simply start Redis with:

```bash
sudo service redis-server start
```

But if you want to use custom Redis settings (e.g., for Docker or memory tuning), you can start Redis using the included config:

```bash
redis-server config/redis.conf
```

This file is not required for local development, but is included for future flexibility.

---

## Flask SECRET_KEY

The `SECRET_KEY` is used by Flask for securely signing session cookies and other security-related features.

### Local Development
For testing purposes, you can use any string:
```env
SECRET_KEY=dev-secret-key-12345
```

### Production Use
In production, you should generate a long random key:

---

## Running the App: `flask run` vs. `python run.py`

You can run the app either way — both are valid depending on context:


### Recommended for Development
```bash
flask run
```

This loads the app based on `FLASK_APP` and `FLASK_ENV` from your `.env`, and enables CLI commands like:
```bash
flask db migrate
flask shell
```

---
--- 

## Database Migrations (Flask-Migrate + Alembic)

run these commands from the backend folder:

```bash
# Generate a new migration (from backend/)
flask db migrate -m "describe your change here"

# Apply the migration to your database
flask db upgrade
```

`alembic.ini` is in the `migrations/` folder and root due to inconsistencies in alembic and flask documentation.

### Post-Deployment: Run DB Migrations in Docker
Once your containers are running, you need to apply the database schema using Flask-Migrate:
```bash
docker exec -it backend flask db upgrade
```
