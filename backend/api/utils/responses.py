# backend/api/utils/responses.py

"""
Utility functions for standardizes API responses
"""

from flask import jsonify

def success_response(data=None, message=None, status_code=200):
    """
    Create a standardizes success response

    Args:
        data: Response data
        message: Response message
        status_code: HTTP status code

    Returns:
        Flask response with JSON data
    """
    response = {
        'success': True
    }

    if message:
        response['message'] = message

    if data is not None:
        response['data'] = data

    return jsonify(response), status_code

def error_response(message, status_code=400, errors=None):
    """
    Create a standardized error response

    Args:
        message: Error message
        status_code: HTTP status code
        errors: Additional error details

    Returns:
        Flask response with JSON data
    """
    response = {
        'success': False,
        'message': message
    }

    if errors:
        response['errors'] = errors

    return jsonify(response), status_code

# error handler functions

def handle_not_found(e):
    """Handle 404 errors"""
    return error_response('Resource not found', 404)

def handle_servor_error(e):
    """Handle 500 errors"""
    return error_response('Internal server error', 500)

def handle_validation_error(errors):
    """Handle validation errors"""
    return error_response('Validation error', 422, errors)