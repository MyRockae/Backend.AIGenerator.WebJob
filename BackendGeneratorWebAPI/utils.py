from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Get the default response first.
    response = exception_handler(exc, context)

    # If there's a response and the exception has a custom method,
    # reformat the output.
    if response is not None and hasattr(exc, 'get_full_details'):
        response.data = exc.get_full_details()
    return response