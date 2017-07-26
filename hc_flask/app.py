from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restplus import Api, Resource, reqparse

from hc_flask.database import db_session
from hc_flask.models.screenresolution import ScreenResolution


app = Flask(__name__)
admin = Admin(app)
admin.add_view(ScreenResolution.get_admin_view())
# ScreenResolution.register_routes(app)


api = Api(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@api.route('/v1/screenresolution')
class ScreenResolutionResource(Resource):
    @api.expect([ScreenResolution.InputSchema])
    def put(self):
        return ScreenResolution.put_endpoint()


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
