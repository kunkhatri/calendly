from flask import request, jsonify, Response, Blueprint
from calendly.factories.controller_factory import ControllerFactory
from calendly.misc.constants import USER_CONTROLLER_KEY

users_bp = Blueprint('users', __name__)

@users_bp.route("/hello")
@users_bp.route("/", methods=["GET"])
def hello():
    return "<h1>Hi, I'm Calendly!</h1>"

@users_bp.route("/user", methods=["POST"])
def add_user():
    controller = ControllerFactory.create(USER_CONTROLLER_KEY)
    return jsonify(controller.add_user(request))

@users_bp.route("/user/<user_id>/get_availability", methods=["GET"])
def get_availability(user_id: str):
    """
    query_params:
        tz: timezone
        filter:
            period_type: exact | range
            period:
                exact:
                    today
                    tomorrow
                    current_week
                    next_week
                    current_month
                    next_month
                range:
                    date1 -> date2

    response:
        slots in unit:
    """
    controller = ControllerFactory.create(USER_CONTROLLER_KEY)
    return jsonify(controller.get_availability(user_id, request))

@users_bp.route("/user/<user_id>/set_availability", methods=["POST"])
def set_availability(user_id: str):
    """
    request payload:
        timezone
        availability:
            type:
                per_date | pattern
            slots:
                per_date:
                    date1:
                        [(9, 11), (14, 15)]
                    date2:
                        [(14, 15), (18, 19)]
                pattern:
                    date: date1
                    slots: [(9, 11), (14, 15)]]
                    repeat_schedule: cron schedule like pattern
                        * * *:
                            first * -> day of the month
                            second * -> month
                            third * -> day of the week

    """
    controller = ControllerFactory.create(USER_CONTROLLER_KEY)
    return jsonify(controller.set_availability(user_id, request))

@users_bp.route("/user/<user_id1>/remove_availability", methods=["POST"])
def remove_availability(user_id: str):
    return Response("Not implemented.", status=501)

@users_bp.route("/user/<user_id1>/overlapping_slots/<user_id2>", methods=["GET"])
def overlapping_available_slots(user_id1, user_id2):
    """
    query params:
        tz: timezone
        filter:
            period_type: exact | range
            period:
                exact:
                    today
                    tomorrow
                    current_week
                    next_week
                    current_month
                    next_month
                range:
                    date1 -> date2
    """
    controller = ControllerFactory.create(USER_CONTROLLER_KEY)
    return jsonify(controller.overlapping_available_slots(user_id1, user_id2, request))

@users_bp.route("/user/<user_id1>/book_slot", methods=["POST"])
def book_slot(user_id: str):
    return Response("Not implemented.", status=501)