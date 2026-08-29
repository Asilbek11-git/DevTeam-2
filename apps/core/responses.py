"""
Standardized API response helper for DevTeam SaaS.
Mandated structure:
{
  "success": bool,
  "message": str,
  "data": dict | list | None,
  "errors": list | dict | None
}
"""
from rest_framework.response import Response
from rest_framework import status

def api_response(success=True, message="", data=None, errors=None, status_code=status.HTTP_200_OK):
    """Generate consistent API response JSON across all endpoints."""
    payload = {
        "success": success,
        "message": message,
        "data": data,
        "errors": errors
    }
    return Response(payload, status=status_code)

def success_response(data=None, message="Operation completed successfully", status_code=status.HTTP_200_OK):
    return api_response(success=True, message=message, data=data, errors=None, status_code=status_code)

def error_response(message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return api_response(success=False, message=message, data=None, errors=errors if errors is not None else [message], status_code=status_code)
