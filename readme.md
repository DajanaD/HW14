Skip to content
GoIT-Python-Web
/
rest-api-tests

Type / to search

Code
Issues
Pull requests
Actions
Projects
Security
Insights
Files
Go to file
t
_static content loaded
docs
migrations
src
tests
.coverage
.gitignore
Procfile
alembic.ini
docker-compose.yml
main.py
pyproject.toml
readme.md
requirements.txt
test.db
Breadcrumbsrest-api-tests
/readme.md
Latest commit
Krabaton
Krabaton
fix readme
55de13d
 · 
last year
History
File metadata and controls

Preview

Code

Blame
49 lines (36 loc) · 876 Bytes
# Реалізація проекту

Для роботи проекта необхідний файл `.env` зі змінними оточення.
Створіть його з таким вмістом і підставте свої значення.

```dotenv
# Database PostgreSQL
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

# JWT authentication
SECRET_KEY=
ALGORITHM=

# Email service
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

# Redis
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=

# Cloud Storage
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

Запуск баз даних


```bash
docker-compose up -d
```

Запуск застосунку


```bash
uvicorn main:app --reload
```
rest-api-tests/readme.md at main · GoIT-Python-Web/rest-api-tests