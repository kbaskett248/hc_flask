from flask import Flask, request, jsonify

from hc_flask.database import db_session
from hc_flask.models.screenresolution import ScreenResolution


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/v1/screenresolution', methods=['POST'])
def post_screenresolution():
    json = request.get_json()
    sr = ScreenResolution.get(session=db_session, client=json['client'])
    if sr is None:
        sr = ScreenResolution.create(session=db_session, **json)
        return f"{sr!r} was created"
    sr.update(session=db_session, **json)
    return f"{sr!r} was updated"

@app.route('/v1/screenresolution/<client>', methods=['GET'])
def get_screenresolution(client):
    sr = ScreenResolution.get(session=db_session, client=client)
    if sr is None:
        return None
    return jsonify(sr.to_dict())
