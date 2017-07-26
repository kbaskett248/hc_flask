from datetime import datetime
from importlib import import_module
from typing import List

from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite:///tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


class Base(object):
    site = None
    created = None
    updated = None

    columns_to_omit_from_repr = ('created', 'updated')

    def __repr__(self):
        values = ['{}={}'.format(name, getattr(self, name))
                  for name in self.get_attributes()
                  if name not in self.columns_to_omit_from_repr]
        return '{}<{}>'.format(self.__class__.__name__, ', '.join(values))


class SqlAlchemy(Base):
    site = Column(String, primary_key=True, default="M0000")
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def get_columns(cls):
        return inspect(cls).columns

    @classmethod
    def get_primary_keys(cls, include_defaults=True):
        def condition(col) -> bool:
            return col.primary_key and (include_defaults or (col.default is None))
        return filter(condition, cls.get_columns())

    @classmethod
    def create(cls, session, **kwargs):
        entity = cls(**kwargs)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    @classmethod
    def query_from_db(cls, session, **kwargs):
        def col_value(col):
            if col.default is not None:
                if col.default.is_callable:
                    return col.default.arg()
                else:
                    return col.default.arg
            else:
                return kwargs[col.name]
        args = {col.name: col_value(col) for col in cls.get_primary_keys()}
        return session.query(cls).filter_by(**args).first()

    def update(self, session, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        session.add(self)
        session.commit()

    @classmethod
    def get_keys(cls):
        return [key.name for key in cls.get_primary_keys(include_defaults=True)]

    @classmethod
    def get_non_default_keys(cls):
        return [key.name for key in cls.get_primary_keys(include_defaults=False)]

    @classmethod
    def get_attributes(cls):
        return [col.name for col in cls.get_columns()]

    def to_dict(self):
        return {name: getattr(self, name) for name in self.get_attributes()}


SqlAlchemyBase = declarative_base(cls=SqlAlchemy)
SqlAlchemyBase.query = db_session.query_property()


def init_db() -> None:
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import_models()
    SqlAlchemyBase.metadata.create_all(bind=engine)


def import_models() -> None:
    for mod in get_models():
        import_module(mod)


def get_models() -> List[str]:
    return [
        'hc_flask.models.screenresolution'
    ]
