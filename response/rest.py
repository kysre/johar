from rest_framework import status
from rest_framework.response import Response


class OkResponse(Response):
    def __init__(self, **kwargs):
        """
        :type data: dict
        """
        super().__init__(status=status.HTTP_200_OK)
        if kwargs is None:
            kwargs = {}
        if 'status' not in kwargs:
            kwargs['status'] = 'ok'
        self.data = kwargs


class NotFoundResponse(Response):
    def __init__(self, **kwargs):
        """
        :type data: dict
        """
        super().__init__(status=status.HTTP_404_NOT_FOUND)
        if kwargs is None:
            kwargs = {}
        if 'status' not in kwargs:
            kwargs['status'] = 'Not Found'
        self.data = kwargs


class CreateUserSuccessResponse(Response):
    def __init__(self, message):
        data = {'message': message}
        super().__init__(data=data, status=status.HTTP_201_CREATED)


class CreateUserErrorResponse(Response):
    def __init__(self, message, errors):
        data = {'message': message, 'errors': errors}
        super().__init__(data=data, status=status.HTTP_400_BAD_REQUEST)


class LoginSuccessResponse(Response):
    def __init__(self, username, token_key, **kwargs):
        """
        :type username: str
        :type token_key: str
        """
        super().__init__(status=status.HTTP_200_OK)
        self.data = {
            'username': username,
            'token': token_key,
        }


class LoginErrorResponse(Response):
    def __init__(self, message, **kwargs):
        """
        :type message: str
        """
        super().__init__(status=status.HTTP_401_UNAUTHORIZED)
        self.data = {
            'error': 'login_failed',
            'message': message,
        }
