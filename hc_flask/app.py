from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_apispec import use_kwargs, marshal_with, FlaskApiSpec
from webargs import fields

from hc_flask.database import db_session
from hc_flask.models.screenresolution import ScreenResolution


app = Flask(__name__)
docs = FlaskApiSpec(app)
admin = Admin(app)
admin.add_view(ScreenResolution.get_admin_view())
ScreenResolution.register_routes(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# @app.route('/v1/screenresolution', methods=['POST'])
# @use_kwargs({'client': fields.Str(), 'hor_res': fields.Int(), 'ver_res': fields.Int()})
# def post_screenresolution():
#     json = request.get_json()
#     sr = ScreenResolution.get(session=db_session, client=json['client'])
#     if sr is None:
#         sr = ScreenResolution.create(session=db_session, **json)
#         return f"{sr!r} was created"
#     sr.update(session=db_session, **json)
#     return f"{sr!r} was updated"

# docs.register(post_screenresolution)
