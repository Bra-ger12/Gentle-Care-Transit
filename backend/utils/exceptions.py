from rest_framework.exceptions import APIException

class CustomException(APIException):
    """
    Base custom exception for Gentle Care Transit.
    """
    status_code = 400
    default_detail = 'An error occurred.'

class BookingException(CustomException):
    """
    Exception raised for booking-related errors.
    """
    pass

class PaymentException(CustomException):
    """
    Exception raised for payment-related errors.
    """
    status_code = 402

class LocationException(CustomException):
    """
    Exception raised for location-related errors.
    """
    pass
