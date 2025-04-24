# Django CRUD Example with React Frontend

This project is a full-stack application with a Django REST API backend and React frontend for managing employees and tasks.

## Project Structure

```
django_crud_example/
├── backend/             # Django REST API
│   ├── core/           # Django project settings
│   ├── employees/      # Employees app
│   ├── tasks/          # Tasks app
│   ├── manage.py       # Django management script
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile      # Backend Docker configuration
└── frontend/           # React frontend (to be created)
```

## Backend (Django REST API)

### API Endpoints

1. Employees API:
   - GET /api/employees/ - List all employees
   - POST /api/employees/ - Create new employee
   - GET /api/employees/{id}/ - Get employee details
   - PUT /api/employees/{id}/ - Update employee
   - DELETE /api/employees/{id}/ - Delete employee

2. Tasks API:
   - GET /api/tasks/ - List all tasks
   - POST /api/tasks/ - Create new task
   - GET /api/tasks/{id}/ - Get task details
   - PUT /api/tasks/{id}/ - Update task
   - DELETE /api/tasks/{id}/ - Delete task

### Setup and Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   cd backend
   docker build -t django-crud-api .
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up
   ```

## Frontend (React)

Coming soon...

## Development

- Python 3.8+
- Django 4.2
- Django REST Framework 3.14
- React (upcoming)

## Testing

Run the test suite:
```bash
cd backend
pytest
```

## Logging

The application includes comprehensive logging for both APIs:
- Employee API logs in `logs/employees.log`
- Task API logs in `logs/tasks.log`
