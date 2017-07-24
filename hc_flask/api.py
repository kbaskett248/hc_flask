from typing import Any, Callable, List, NamedTuple

from hc_flask.database import db_session

class ApiBase(object):
    STATUS_CREATED = "created"
    STATUS_UPDATED = "updated"

    class PutResult(NamedTuple):
        entity: Any
        status: str

    class Route(NamedTuple):
        route: str
        operation: str
        function: Callable

    @classmethod
    def put_endpoint(cls, body, **kwargs) -> List['ApiBase.PutResult']:
        return [cls.put_individual(b, **kwargs) for b in body]

    @classmethod
    def put_individual(cls, body, **kwargs) -> 'ApiBase.PutResult':
        body.update(kwargs)
        entity = cls.get(**body)
        if entity:
            entity.update(**body)
            return cls.PutResult(entity, cls.STATUS_UPDATED)
        
        entity = cls.create(**body)
        return cls.PutResult(entity, cls.STATUS_CREATED)

    @classmethod
    def routes(cls) -> List['ApiBase.Route']:
        put_route = f'/v1/{cls.__name__.lower()}'
        return [
            cls.Route(put_route, 'PUT', cls.put_endpoint)
        ]

from flask import Flask, request, jsonify, Response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from hc_flask.database import db_session

class FlaskApi(ApiBase):
    class BaseModelView(ModelView):
        can_create = False
        can_edit = False
        can_delete = False
        column_display_pk = True
        column_filters = ['site']
        can_export = True
        can_view_details = True
        export_types = ['Excel', 'CSV', 'TSV']

    AdminView = BaseModelView

    @classmethod
    def put_endpoint(cls, body) -> Response:
        results = super(FlaskApi, cls).put_endpoint(session=db_session, body=body)
        return jsonify(
            [{cls.__name__: result.entity.to_dict(),
              'status': result.status}
             for result in results]
        )

    @classmethod
    def register_routes(cls, app: Flask) -> None:
        for route in cls.routes():
            app.add_url_rule(route.route,
                             endpoint=f"post_{cls.__name__}",
                             view_func=route.function,
                             methods=[route.operation])

    @classmethod
    def get_admin_view(cls) -> AdminView:
        return cls.AdminView(cls, db_session)
