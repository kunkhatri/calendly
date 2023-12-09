from calendly.misc.exceptions import ObjectNotFoundException, BadRequestException
from calendly import app
from flask import request, jsonify
from calendly.factories.controller_factory import ControllerFactory
from calendly.misc.constants import USER_CONTROLLER_KEY

@app.route("/hello")
@app.route("/", methods=["GET"])
def hello():
    return "<h1>Hi, I'm Calendly!</h1>"


@app.route("/user/<user_id>/get_availability", methods=["GET"])
def get_availability(user_id):
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

@app.route("/user/<user_id>/set_availability", methods=["POST"])
def set_availability(user_id):
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

@app.route("/user/<user_id1>/overlapping_slots/<user_id2>", methods=["GET"])
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


######## exception handlers #################

@app.errorhandler(ObjectNotFoundException)
def handle_not_found(e):
    return "Not found!", 404

@app.errorhandler(BadRequestException)
def handle_bad_request(e):
    return "Bad request!", 400
