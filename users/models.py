from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Employee(models.Model):

    account_types = [
        ('type1', 'type1'),
        ('type2', 'type2'),
        ('type3', 'type3'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Django's default user model to be extended")
    phone_number = PhoneNumberField(help_text='Phone number of the employee')
    department = models.CharField(max_length=200, help_text='The department where the employee works')
    account_type = models.CharField(
        max_length=5, 
        choices=account_types, 
        help_text='The account type of the employee registered',
    )

    def __str__(self) -> str:
        
        return self.user.username
