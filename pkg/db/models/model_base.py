from ..database import BASE, ENGINE
from sqlalchemy.engine.reflection import Inspector


class ModelUtils(object):

    __tablename__ = None

    _inspector = Inspector.from_engine(ENGINE)

    @classmethod
    def create_table(cls):
        # create the table only if it does not exists
        if cls.__tablename__ not in cls._inspector.get_table_names():
            BASE.metadata.tables[cls.__tablename__].create(bind=ENGINE)

    def to_dict(self):
        ret_dict = self.__dict__.copy()

        # remove this key for JSON serializable
        if '_sa_instance_state' in ret_dict:
            ret_dict.pop('_sa_instance_state', None)

        return ret_dict