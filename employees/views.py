import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Employee
from .serializers import EmployeeSerializer

# Get logger for employees app
logger = logging.getLogger('employees')

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    queryset = Employee.objects.all().order_by('-date_of_joining')
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        logger.info('Fetching list of all employees')
        try:
            response = super().list(request, *args, **kwargs)
            logger.info(f'Successfully retrieved {self.get_queryset().count()} employees')
            return response
        except Exception as e:
            logger.error(f'Error fetching employees list: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info('Creating new employee')
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f'Successfully created employee: {response.data.get("full_name")} (ID: {response.data.get("employee_id")})')
            return response
        except ValidationError as e:
            logger.warning(f'Validation error in employee creation: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error creating employee: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        logger.info(f'Updating employee with ID: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            logger.info(f'Current employee data before update: {instance.__dict__}')
            response = super().update(request, *args, **kwargs)
            logger.info(f'Successfully updated employee: {response.data.get("full_name")} (ID: {response.data.get("employee_id")})')
            return response
        except ValidationError as e:
            logger.warning(f'Validation error in employee update: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error updating employee: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'Deleting employee with ID: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            employee_info = f'{instance.full_name} (ID: {instance.employee_id})'
            response = super().destroy(request, *args, **kwargs)
            logger.info(f'Successfully deleted employee: {employee_info}')
            return response
        except Exception as e:
            logger.error(f'Error deleting employee: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
