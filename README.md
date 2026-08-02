# Store API

A RESTful e-commerce backend built with **Django REST Framework**. This project demonstrates modern backend development practices, including JWT authentication, service-layer architecture, Docker, PostgreSQL, API documentation, and automated testing.

---

## Features
 
* JWT Authentication (Djoser + SimpleJWT)
* User registration and authentication
* Product management
* Category management
* Product reviews
* Order creation and management
* Inventory validation
* Automatic order total calculation
* Role-based permissions
* Pagination
* Swagger/OpenAPI documentation
* Docker support
* PostgreSQL database
* Automated tests with Pytest

---

## Tech Stack

* Python 3
* Django
* Django REST Framework
* PostgreSQL
* Docker & Docker Compose
* Djoser
* SimpleJWT
* drf-spectacular (Swagger)
* Pytest

---

## Project Structure

```
apps/
├── categories/
├── products/
├── reviews/
├── orders/
└── users/

config/
tests/
```

---

## API Endpoints

| Endpoint              | Description       |
| --------------------- | ----------------- |
| `/api/categories/`    | Categories        |
| `/api/products/`      | Products          |
| `/api/review/`        | Reviews           |
| `/api/orders/`        | Orders            |
| `/api/users/`         | User management   |
| `/api/token/`         | Obtain JWT token  |
| `/api/token/refresh/` | Refresh JWT token |
| `/api/docs/`          | Swagger UI        |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/store-api.git
cd store-api
```

Create a `.env` file using `.env.example`.

Run the project with Docker:

```bash
docker compose up --build
```

Apply migrations:

```bash
docker compose exec web python manage.py migrate
```

Create a superuser (optional):

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Running Tests

Run all tests:

```bash
docker compose exec web pytest
```

---

## API Documentation

After starting the project, Swagger documentation is available at:

```
http://localhost:8000/api/docs/
```

---

## Architecture

The project follows a service-layer architecture where business logic is separated from views and serializers.

Main concepts used:

* Service layer
* Django ORM
* ModelViewSets
* Serializers
* JWT Authentication
* Custom permissions
* Database transactions
* Pagination
* Automated testing

---

## Testing

The project includes automated tests for:

* Categories
* Products
* Reviews
* Orders
* Permissions
* Authentication
* Business logic

---

## Author

Developed as a portfolio project to practice backend development with Django REST Framework.
