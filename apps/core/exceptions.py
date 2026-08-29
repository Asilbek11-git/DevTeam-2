"""
Centralized DRF Exception Handler.
Ensures all errors return the standard payload format:
{
  "success": false,
  "message": "...",
  "data": null,
  "errors": [...]
}
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated, NotFound, Throttled
from rest_framework import status

class PlanLimitExceededException(Exception):
    """Raised when a workspace attempts an action exceeding its subscription tier."""
    def __init__(self, message="Your current plan limit has been reached. Please upgrade to unlock this feature."):
        self.message = message
        super().__init__(self.message)

class DependencyCycleException(Exception):
    """Raised when adding a task dependency would create a circular loop."""
    def __init__(self, message="Dependency loop detected. Cannot block tasks circularly."):
        self.message = message
        super().__init__(self.message)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        if isinstance(response.data, dict):
            for key, val in response.data.items():
                if isinstance(val, list):
                    errors.extend([f"{key}: {item}" for item in val])
                else:
                    errors.append(f"{key}: {val}")
        elif isinstance(response.data, list):
            errors = response.data
        else:
            errors = [str(response.data)]

        message = "Validation failed" if response.status_code == status.HTTP_400_BAD_REQUEST else str(exc)
        
        response.data = {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors
        }
        return response

    # Handle custom domain exceptions
    if isinstance(exc, PlanLimitExceededException):
        from .responses import error_response
        return error_response(message=exc.message, errors=[exc.message], status_code=status.HTTP_402_PAYMENT_REQUIRED)

    if isinstance(exc, DependencyCycleException):
        from .responses import error_response
        return error_response(message=exc.message, errors=[exc.message], status_code=status.HTTP_409_CONFLICT)

    return None
