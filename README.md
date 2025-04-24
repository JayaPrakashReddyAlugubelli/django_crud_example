# Django CRUD Example

A comprehensive Django application demonstrating CRUD operations with task and employee management, featuring a robust logging system.

## Features

### Task Management
- List all tasks
- Create new tasks
- Update existing tasks
- Delete tasks
- Mark tasks as completed
- Bootstrap-based responsive UI

### Employee Management
- List all employees
- Register new employees
- Update employee information
- Delete employee records
- Validation for email and phone number formats
- Comprehensive employee details (personal info, job details)

### Logging System
- Separate log files for tasks and employees APIs
- Request/response logging with timing information
- Detailed error logging with stack traces
- Organized log directory structure
- Log rotation and management
- Performance monitoring

## Installation
1. Clone the repository:
```bash
git clone https://github.com/JayaPrakashReddyAlugubelli/django_crud_example.git
cd django_crud_example
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver
```

5. Visit http://127.0.0.1:8000 in your browser

## Project Structure
```
django_crud_example/
├── core/                   # Project settings and configuration
├── tasks/                  # Task management app
├── employees/              # Employee management app
└── logs/                   # Application logs
    ├── tasks/             # Task-specific logs
    ├── employees/         # Employee-specific logs
    └── general/           # General application logs
```

## Running Tests
To run the tests:
```bash
pytest tasks/tests/test_views.py -v
pytest employees/tests/test_views.py -v
```

## Production Deployment
1. Set the following environment variables:
   - DJANGO_SECRET_KEY
   - DJANGO_SETTINGS_MODULE=core.settings_prod

2. Update ALLOWED_HOSTS in settings_prod.py with your domain

3. Configure logging paths in production:
   - Ensure log directories exist and have proper permissions
   - Configure log rotation if needed
   - Monitor log files for issues and performance

## Security Features
- CSRF protection enabled
- Form validation and sanitization
- Secure password handling
- Production settings separation
- Sensitive data filtering in logs

## License
MIT License
