# SOS Tracker System - Where Are My People

A simple backend system for tracking users and their SOS devices in real-time using Django, Django REST Framework, Docker, and PostgreSQL.

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/sos-tracker-system.git
cd sos-tracker-system
```

2. **Copy environment file and edit it to set your credentials**

```bash
cp .env.example .env
```

3. **Build and start the services**

```bash
docker compose up --build -d
```

4. **Make and apply migrations**

```bash
docker compose run web python manage.py makemigrations
docker compose run web python manage.py migrate
```

5. **Create a superuser (optional, for admin panel access)**

```bash
docker compose run web python manage.py createsuperuser
```

5. **Visit the API docs and admin panel**

- Swagger UI: http://localhost:8000/swagger/
- Redoc UI: http://localhost:8000/redoc/
- Admin Panel: http://localhost:8000/admin/

---

## If I had more time, I would:

- Add simple saving logs to files,
- Add errors in another file to make them more generic,
- Add Celery and Redis to offload location pings,
- Add authentication,
- Add unit tests.

## To prevent a device from overwhelming the backend with too many pings (e.g. every second instead of every few minutes), I would:

- Use Celery + Redis for buffering and throttle task execution.
- Add rate limiting per device (e.g., no more than 1 ping per 30 seconds).
- Validate timestamps on the backend and ignore outdated or too-frequent pings.
- Implement mechanism of deleting old not relevant pings from database.
