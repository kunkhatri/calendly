from calendly.rest import CalendlyRestInterface
from calendly.factories.service_factory import ServiceFactory
from calendly.misc.constants import USER_SERVICE_KEY
from calendly.services import CalendlyService
from calendly.dtos.user_availability_filter import UserAvailabilityFilter
from calendly.dtos.availability_config import AvailabilityConfig
from calendly.misc.exceptions import BadRequestException
import json

class UserRestController(CalendlyRestInterface):
    def __init__(self):
        self.user_service: CalendlyService = ServiceFactory.create(USER_SERVICE_KEY)

    def add_user(self, request) -> dict:
        if not request.data:
            raise BadRequestException("Invalid request, no data provided to add user.")

        request_body = json.loads(request.data)
        response = self.user_service.add_user(request_body)
        return response

    def get_availability(self, user_id, request) -> dict:
        timezone = request.args.get("timezone")
        # default to today
        filter_dict = {
            "type": "NAME",
            "value": "TODAY",
        }
        if request.args.get("filter"):
            filter_dict = json.loads(request.args.get("filter"))
        response = self.user_service.get_availability(
            user_id, UserAvailabilityFilter.to_object(filter_dict), timezone=timezone
        )
        return response

    def set_availability(self, user_id, request):
        if not request.data:
            raise BadRequestException("Invalid request, no availability provided.")

        request_body = json.loads(request.data)
        if "availability_slots" not in request_body:
            raise BadRequestException("Invalid request, no availability provided.")

        timezone = request_body.get("timezone")
        availability_config = request_body.get("availability_slots")
        self.user_service.set_availability(
            user_id,
            AvailabilityConfig.to_object(availability_config),
            timezone=timezone
        )
        return {
            "response": f"Successfully set availability for user {user_id}.",
            "status": 200,
        }

    def overlapping_available_slots(self, user_id1, user_id2, request):
        timezone = request.args.get("timezone")
        # default to today
        filter_dict = {
            "type": "NAME",
            "value": "TODAY",
        }
        if request.args.get("filter"):
            filter_dict = json.loads(request.args.get("filter"))

        response = self.user_service.get_overlapping_available_slots(
            user_id1, user_id2, UserAvailabilityFilter.to_object(filter_dict), timezone=timezone
        )
        return response

