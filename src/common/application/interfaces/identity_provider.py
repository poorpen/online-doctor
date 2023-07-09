from typing import Protocol

from src.common.domain.models.access import Access


class IdentityProvider(Protocol):

    def get_access_policy(self) -> Access:
        raise NotImplemented
