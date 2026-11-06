# Workout Tracking API

A RESTful API built with Flask that allows users to manage exercises and track their workouts. The API supports creating, viewing, updating, and deleting workout records, with exercises organized by category and equipment requirements.

## Features

- Create, retrieve, update, and delete exercises.
- Create and manage workout records.
- Organize exercises by category.
- Track equipment requirements.
- Associate workouts with exercises.
- Validate and serialize data using Marshmallow.
- Store application data in a relational database.

## Technologies Used

- **Python** – Backend programming language.
- **Flask** – Web framework.
- **Flask-SQLAlchemy** – Database management and ORM.
- **Flask-Migrate** – Database migrations.
- **Marshmallow** – Data serialization and validation.
- **SQLite** – Database storage.

## Project Structure

```text
workout-tracking-api/
│
├── app.py
├── models.py
├── schemas.py
├── migrations/
├── instance/
├── seed.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd workout-tracking-api
```

### 2. Install Dependencies

If using Pipenv:

```bash
pipenv install
```

### 3. Activate the Virtual Environment

```bash
pipenv shell
```

### 4. Set Up the Database

Run the database migrations:

```bash
flask db upgrade
```

### 5. Seed the Database

If the project includes the seed script:

```bash
python seed.py
```

### 6. Run the Application

```bash
python app.py
```

The API will run locally at:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve a specific exercise |
| POST | `/exercises` | Create a new exercise |
| PATCH | `/exercises/<id>` | Update an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve a specific workout |
| POST | `/workouts` | Create a new workout |
| PATCH | `/workouts/<id>` | Update a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

## Testing

API endpoints can be tested using Postman.

Send requests to the local server and inspect the JSON responses and HTTP status codes.

## Future Improvements

- User authentication and authorization.
- Workout progress tracking.
- Exercise performance statistics.
- Workout scheduling.

## Author

Developed as a backend development project using Python and Flask.
