from rest_framework.authentication import TokenAuthentication

class BearerAuthentication(TokenAuthentication):
    """
    This class simply changes the expected token keyword to 'Bearer'
    from the Django rest authentication default 'Token'. This allows
    applications like Postman to work with token authentication.
    """
    keyword = "Bearer"
