from rest_framework.schemas import AutoSchema
import coreapi
import coreschema


class EmployeesSchema(AutoSchema):

    manual_fields = []

    def get_manual_fields(self, path, method):
        
        custom_fields = []

        if method.lower() == 'get':
            return custom_fields

        if method.lower() == 'post':
            custom_fields = [
                coreapi.Field(
                    'phone_number',
                    required=True,
                    location='form',
                    schema=coreschema.String(description='Valid phone number'),
                ),
                coreapi.Field(
                    'department',
                    required=True,
                    location='form',
                    schema=coreschema.String(description='The department where the employee belongs to'),
                ),
                coreapi.Field(
                    'account_type',
                    required=True,
                    location='form',
                    schema=coreschema.String(description='Available types are: type1, type2 and type3')
                )
            ]
            return self._manual_fields + custom_fields