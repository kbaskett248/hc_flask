from sqlalchemy import Column, Integer, String
from flask_apispec import use_kwargs, marshal_with
from flask_restplus import api
from marshmallow import Schema, fields
from webargs.flaskparser import use_args

from hc_flask.api import FlaskApi
from hc_flask.database import SqlAlchemyBase


class ScreenResolution(SqlAlchemyBase, FlaskApi):
    """Defines the table and API for a ScreenResolution log entry."""

    client = Column(String(255), primary_key=True)
    hor_res = Column(Integer)
    ver_res = Column(Integer)

    class InputSchema(Schema):
        client = fields.Str(required=True)
        hor_res = fields.Int(required=True)
        ver_res = fields.Int(required=True)

    @classmethod
    @use_args(InputSchema(many=True, strict=True),
              locations=('json', ))
    def put_endpoint(cls, body):
        return super(ScreenResolution, cls).put_endpoint(body)

    def __str__(self):
        return "{site}\\{client} ({hor_res}x{ver_res})".format(**self.to_dict())

