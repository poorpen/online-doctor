from abc import ABC, abstractmethod

from sqlalchemy.sql.selectable import Select


class BaseQueryBuilder(ABC):

    def __init__(self):
        self._query = None

    def _build(self) -> Select:
        return self._query

    @abstractmethod
    def get_query(self, *args, **kwargs) -> Select:
        pass
