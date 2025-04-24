from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'full_name', 'date_of_birth', 'gender', 
            'phone_number', 'email', 'address', 'job_title',
            'department', 'employee_id', 'date_of_joining', 
            'work_location'
        ]
        
    def validate_email(self, value):
        """
        Check that the email is unique
        """
        if self.instance is None:  # Creating new employee
            if Employee.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        else:  # Updating existing employee
            if Employee.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Email already exists")
        return value

    def validate_employee_id(self, value):
        """
        Check that the employee_id is unique
        """
        if self.instance is None:  # Creating new employee
            if Employee.objects.filter(employee_id=value).exists():
                raise serializers.ValidationError("Employee ID already exists")
        else:  # Updating existing employee
            if Employee.objects.filter(employee_id=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Employee ID already exists")
        return value
