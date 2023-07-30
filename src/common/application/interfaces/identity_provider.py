from typing import Protocol

from src.common.domain.models.access import Access


class IIdentityProvider(Protocol):

    def get_access_policy(self) -> Access:
        raise NotImplemented
