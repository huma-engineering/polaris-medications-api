import time

from flask import Blueprint, Response, current_app, jsonify
from flask_batteries_included.helpers.security import protected_route
from flask_batteries_included.helpers.security.endpoint_security import key_present

from .controller import reset_database

development = Blueprint("dhos/dev", __name__)


@development.route("/drop_data", methods=["POST"])
@protected_route(key_present("system_id"))
def drop_data_route() -> Response:

    if current_app.config["ALLOW_DROP_DATA"] is not True:
        raise PermissionError("Cannot drop data in this environment")

    start: float = time.time()
    reset_database()
    total_time: float = time.time() - start
    return jsonify({"complete": True, "time_taken": str(total_time) + "s"})
