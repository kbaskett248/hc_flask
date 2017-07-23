from typing import List

from sqlalchemy import Column, Integer, String

from hc_flask.database import SqlAlchemyBase


class ScreenResolution(SqlAlchemyBase):
    """Defines the table and API for a ScreenResolution log entry."""

    client = Column(String(255), primary_key=True)
    hor_res = Column(Integer)
    ver_res = Column(Integer)

    # @classmethod
    # def get_endpoint(cls, db: SQLAlchemy, client: ClientName):
    #     kwargs = {'client': client}
    #     return super(ScreenResolution, cls).get_endpoint(db, **kwargs)

    # @classmethod
    # def put_endpoint(cls, db: SQLAlchemy, body: Body):
    #     # kwargs = {
    #     #     'client': client,
    #     #     'hor_res': hor_res,
    #     #     'ver_res': ver_res
    #     # }
    #     return super(ScreenResolution, cls).put_endpoint(db, body)

    def __str__(self):
        return "{site}\\{client} ({hor_res}x{ver_res})".format(**self.to_dict())

