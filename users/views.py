from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from .cschemas import EmployeesSchema
from .models import Employee
from .serializers import EmployeeSerializer
import coreapi
import coreschema


class RegisterView(APIView):
    
    schema = ManualSchema(
        [
            coreapi.Field(
                name='username',
                required=True,
                location='form',
                schema=coreschema.String(description='Valid username'),
            ),
            coreapi.Field(
                name='email',
                required=True,
                location='form',
                schema=coreschema.String(description='Valid email'),
            ),
            coreapi.Field(
                name='password',
                required=True,
                location='form',
                schema=coreschema.String(description='Valid password'),
            ),
        ],
        description='Here you can create a new user.',
        encoding='application/json',
    )

    def post(self, request: Request):
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response({'details': 'You are now registered as %s' % username})


class EmployeesView(APIView):

    schema = EmployeesSchema()

    def get(self, request: Request):
        """
        Here you can get an API that contains all the information about the employees.

        The credentials of the registered user should be provided in order to get the information. 
        """

        if 'Authorization' not in request.headers:
            return Response({'result': 'Credentials are not provided!'})
        
        token = request.headers.get('Authorization').split()[-1]
        try:
            Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response({'result': 'You are not allowed to request this page!'})
        employees = EmployeeSerializer(Employee.objects.select_related(), many=True).data
        return Response(employees)


    def post(self, request: Request):
        """
        Here you can create an account for an existing/registered user.

        The credentials of the registered user should be provided in order to get the information. 
        """

        if 'Authorization' not in request.headers:
            return Response({'result': 'Credentials are not provided!'})
        
        token = request.headers.get('Authorization').split()[-1]
        phone_number = request.data.get('phone_number')
        department = request.data.get('department')
        account_type = request.data.get('account_type')
        user = Token.objects.get(key=token).user
        try:
            employee = Employee(
                user=user,
                phone_number=phone_number,
                department=department,
                account_type=account_type,
            )
            employee.save()
        except IntegrityError:
            return Response({'result': 'An account for the user %s has already been created!' % user.username})
        return Response({'status': 'Account for %s has been created!' % user.username})


class ProfileView(APIView):

    def get(self, request: Request):
        """
        Here you can get an API that contains information about a specific registered user.

        You should provide the token of that user, otherwise no information is represented.
        """
        
        if 'Authorization' not in request.headers:
            return Response({'result': 'Credentials are not provided!'})
        
        token = request.headers.get('Authorization').split()[-1]
        try:
            user = Token.objects.get(key=token).user
            profile = EmployeeSerializer(get_object_or_404(Employee, user=user)).data
        except Token.DoesNotExist:
            return Response({'result': 'Invalid token!'})
        except Http404:
            return Response({'result': 'You have not opened a profile yet!'})
        return Response(profile)
