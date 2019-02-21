from rest_framework.response import Response
from rest_framework import status


class ValidationUtility:

    def validate_data_object(self, data_object, field_name, return_object_type):
        value = data_object.get(field_name)

        # check that field_name exists in data_object
        if not value:
            return None, Response(f'{field_name}_field_not_found', status=status.HTTP_400_BAD_REQUEST)

        # attempt casting value to object_type
        try:
            value = return_object_type(value)
        except ValueError:
            return None, Response(f'{field_name}_invalid', status=status.HTTP_400_BAD_REQUEST)

        return value, None
