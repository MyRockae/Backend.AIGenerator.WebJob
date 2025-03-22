from rest_framework.response import Response
from rest_framework import status

class SuccessResponse:
    @staticmethod
    def standard_response(object_instance=None, message="Successfully Completed"):
        if object_instance:
            return {"id": object_instance.id, "message": message}
        else:
            return {"message": message}
