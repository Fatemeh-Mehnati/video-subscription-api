# Video Subscription API

A Django REST Framework API for a video subscription service.

## Features

- User registration and authentication
- JWT-based authentication
- User profile endpoint
- Video and category management
- Subscription plans
- User subscriptions
- Payment records
- Mock payment gateway
- Watch history
- Video ratings
- Comments and replies
- Favorites
- Subscription-based access control
- Real-time video updates using WebSockets
- Swagger / OpenAPI documentation
- Automated model tests

## Tech Stack

- Python
- Django 6.1.1
- Django REST Framework 3.18.1
- Django Channels 4.3.2
- Daphne 4.2.3
- Simple JWT 5.5.1
- django-filter
- drf-spectacular
- Twisted
- SQLite / configured database

## Installation

Clone the repository:

```bash
git clone https://github.com/Fatemeh-Mehnati/video-subscription-api.git
cd video-subscription-api
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser if needed:

```bash
python manage.py createsuperuser
```

## Running the Project

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```

## Authentication

The API uses JWT authentication.

### Register

```text
POST /api/accounts/register/
```

### Login

```text
POST /api/accounts/login/
```

### Refresh Token

```text
POST /api/accounts/token/refresh/
```

### Current User

```text
GET /api/accounts/me/
```

Authenticated requests should include:

```text
Authorization: Bearer <access_token>
```

## API Endpoints

### Accounts

```text
POST /api/accounts/register/
POST /api/accounts/login/
POST /api/accounts/token/refresh/
GET  /api/accounts/me/
```

### Videos

```text
/api/categories/
/api/videos/
/api/favorites/
/api/watch-history/
```

### Comments

```text
GET    /api/videos/<video_id>/comments/
POST   /api/videos/<video_id>/comments/
GET    /api/videos/<video_id>/comments/<comment_id>/
PATCH  /api/videos/<video_id>/comments/<comment_id>/
DELETE /api/videos/<video_id>/comments/<comment_id>/
```

### Subscriptions

```text
/api/plans/
/api/subscriptions/
```

### Payments

```text
/api/payments/
/api/payments/mock-gateway/
```

## Realtime WebSocket

The project uses Django Channels for real-time video updates.

WebSocket endpoint:

```text
/ws/videos/<video_id>/
```

A simple browser-based realtime test page is also available:

```text
/api/realtime-test/?video=<video_id>
```

## Running Tests

Run all automated tests:

```bash
python manage.py test
```

The project currently contains 21 automated tests covering the main models and constraints.

Expected result:

```text
Found 21 test(s).
...
Ran 21 tests ...
OK
```

## ERD

![ERD](docs/erd.png)

The editable Mermaid source is also available at:

```text
docs/erd.mmd
```

## Project Structure

```text
video-subscription-api/
│
├── accounts/
├── videos/
├── subscriptions/
├── payments/
├── config/
├── docs/
│   ├── erd.png
│   └── erd.mmd
├── manage.py
├── requirements.txt
└── README.md
```

## License

This project was developed as a Django REST Framework backend project.