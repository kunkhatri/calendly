from flask import Flask
import os
from calendly.misc.exceptions import ObjectNotFoundException, BadRequestException
from calendly.views import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)


######## exception handlers #################

@app.errorhandler(ObjectNotFoundException)
def handle_not_found(e):
    return "Not found!", 404

@app.errorhandler(BadRequestException)
def handle_bad_request(e):
    return "Bad request!", 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
