from abc import ABC


class DBGateway(ABC):

    def commit(self) -> None:
        raise NotImplemented

    def rollback(self) -> None:
        raise NotImplemented
