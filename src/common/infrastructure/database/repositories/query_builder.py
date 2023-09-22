from abc import ABC

from sqlalchemy.sql.selectable import Select


class BaseQueryBuilder(ABC):

    def __init__(self, query: Select):
        self._query = query

    def build(self) -> Select:
        return self._query
