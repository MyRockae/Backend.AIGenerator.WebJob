from django.views.decorators.csrf import csrf_exempt
import threading
from django.http import JsonResponse, HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from functools import wraps

# Import your worker function.
from apps.worker.utils import start_worker

# Custom decorator with functools.wraps to preserve view metadata.
def api_key_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if provided_key != settings.GENERATOR_API_KEY:
            return HttpResponseForbidden('Invalid API key.')
        return view_func(request, *args, **kwargs)
    return wrapped_view

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="X-API-Key",
            description="API key required for authentication",
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ],
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            },
            "example": {"message": "Worker started."}
        },
        403: {
            "type": "string",
            "example": "Invalid API key."
        }
    },
    description="Endpoint that checks if a worker is running and, if not, starts it.",
    tags=["Worker"]
)
@csrf_exempt
@api_view(['POST'])
@api_key_required
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def trigger_worker_view(request):
    """
    Endpoint that checks if a worker is running and, if not, starts it.
    """
    if cache.get('worker_running'):
        return JsonResponse({"message": "Worker is already running."})
    
    # Start the worker in a background thread.
    threading.Thread(target=start_worker).start()
    return JsonResponse({"message": "Worker started."})
