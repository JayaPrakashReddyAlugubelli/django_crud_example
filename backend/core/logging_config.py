import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Create subdirectories for different components
EMPLOYEE_LOGS = os.path.join(LOGS_DIR, 'employees')
TASK_LOGS = os.path.join(LOGS_DIR, 'tasks')
GENERAL_LOGS = os.path.join(LOGS_DIR, 'general')

for directory in [EMPLOYEE_LOGS, TASK_LOGS, GENERAL_LOGS]:
    os.makedirs(directory, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'employee_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(EMPLOYEE_LOGS, 'employee_api.log'),
            'formatter': 'verbose',
        },
        'employee_error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(EMPLOYEE_LOGS, 'employee_error.log'),
            'formatter': 'verbose',
        },
        'task_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(TASK_LOGS, 'task_api.log'),
            'formatter': 'verbose',
        },
        'task_error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(TASK_LOGS, 'task_error.log'),
            'formatter': 'verbose',
        },
        'general_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(GENERAL_LOGS, 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'general_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'employees': {
            'handlers': ['console', 'employee_file', 'employee_error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'tasks': {
            'handlers': ['console', 'task_file', 'task_error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
