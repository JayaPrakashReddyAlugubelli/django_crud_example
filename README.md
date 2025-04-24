# Django CRUD Example

A simple Django application demonstrating CRUD (Create, Read, Update, Delete) operations with a task management system.

## Features

- List all tasks
- Create new tasks
- Update existing tasks
- Delete tasks
- Mark tasks as completed
- Bootstrap-based responsive UI

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

## Running Tests

To run the tests:
```bash
pytest tasks/tests/test_views.py -v
```

## Production Deployment

1. Set the following environment variables:
   - DJANGO_SECRET_KEY
   - DJANGO_SETTINGS_MODULE=core.settings_prod

2. Update ALLOWED_HOSTS in settings_prod.py with your domain

## License

MIT License
