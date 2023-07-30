from abc import ABC


class IDBGateway(ABC):

    def commit(self) -> None:
        raise NotImplemented

    def rollback(self) -> None:
        raise NotImplemented
