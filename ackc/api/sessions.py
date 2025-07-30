"""Session management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.realms_admin import (
    delete_admin_realms_realm_sessions_session,
    get_admin_realms_realm_client_session_stats,
)
from ..generated.api.clients import (
    get_admin_realms_realm_clients_client_uuid_session_count,
    get_admin_realms_realm_clients_client_uuid_user_sessions,
    get_admin_realms_realm_clients_client_uuid_offline_sessions,
    get_admin_realms_realm_clients_client_uuid_offline_session_count,
)
from ..generated.api.users import (
    get_admin_realms_realm_users_user_id_sessions,
    get_admin_realms_realm_users_user_id_offline_sessions_client_uuid,
)
from ..generated.models import UserSessionRepresentation
from ..generated.types import UNSET, Unset

__all__ = "SessionsAPI", "SessionsClientMixin", "UserSessionRepresentation"


class SessionsAPI(BaseAPI):
    """Session management API methods."""

    # Realm session operations
    def get_client_session_stats(self, realm: str | None = None) -> list | None:
        """Get client session statistics for a realm (sync)."""
        return self._sync(get_admin_realms_realm_client_session_stats.sync, realm)

    async def aget_client_session_stats(self, realm: str | None = None) -> list | None:
        """Get client session statistics for a realm (async)."""
        return await self._async(get_admin_realms_realm_client_session_stats.asyncio, realm)

    def delete_session(self, realm: str | None = None, *, session: str) -> None:
        """Delete a session (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_sessions_session.sync_detailed,
            realm=realm,
            session=session
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete session: {response.status_code}")

    async def adelete_session(self, realm: str | None = None, *, session: str) -> None:
        """Delete a session (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_sessions_session.asyncio_detailed,
            realm=realm,
            session=session
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete session: {response.status_code}")

    # Client session operations
    def get_client_session_count(self, realm: str | None = None, *, client_uuid: str) -> int | None:
        """Get session count for a client (sync)."""
        return self._sync(
            get_admin_realms_realm_clients_client_uuid_session_count.sync,
            realm=realm,
            client_uuid=client_uuid
        )

    async def aget_client_session_count(self, realm: str | None = None, *, client_uuid: str) -> int | None:
        """Get session count for a client (async)."""
        return await self._async(
            get_admin_realms_realm_clients_client_uuid_session_count.asyncio,
            realm=realm,
            client_uuid=client_uuid
        )

    def get_client_user_sessions(
        self,
        realm: str | None = None,
        *,
        client_uuid: str,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
    ) -> list[UserSessionRepresentation] | None:
        """Get user sessions for a client (sync).
        
        Args:
            realm: The realm name
            client_uuid: Client UUID
            first: Pagination offset
            max: Maximum results to return
            
        Returns:
            List of user sessions
        """
        return self._sync(
            get_admin_realms_realm_clients_client_uuid_user_sessions.sync,
            realm=realm,
            client_uuid=client_uuid,
            first=first,
            max_=max,
        )

    async def aget_client_user_sessions(
        self,
        realm: str | None = None,
        *,
        client_uuid: str,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
    ) -> list[UserSessionRepresentation] | None:
        """Get user sessions for a client (async).
        
        Args:
            realm: The realm name
            client_uuid: Client UUID
            first: Pagination offset
            max: Maximum results to return
            
        Returns:
            List of user sessions
        """
        return await self._async(
            get_admin_realms_realm_clients_client_uuid_user_sessions.asyncio,
            realm=realm,
            client_uuid=client_uuid,
            first=first,
            max_=max,
        )

    def get_client_offline_sessions(
        self,
        realm: str | None = None,
        *,
        client_uuid: str,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
    ) -> list[UserSessionRepresentation] | None:
        """Get offline sessions for a client (sync).
        
        Args:
            realm: The realm name
            client_uuid: Client UUID
            first: Pagination offset
            max: Maximum results to return
            
        Returns:
            List of offline user sessions
        """
        return self._sync(
            get_admin_realms_realm_clients_client_uuid_offline_sessions.sync,
            realm=realm,
            client_uuid=client_uuid,
            first=first,
            max_=max,
        )

    async def aget_client_offline_sessions(
        self,
        realm: str | None = None,
        *,
        client_uuid: str,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
    ) -> list[UserSessionRepresentation] | None:
        """Get offline sessions for a client (async).
        
        Args:
            realm: The realm name
            client_uuid: Client UUID
            first: Pagination offset
            max: Maximum results to return
            
        Returns:
            List of offline user sessions
        """
        return await self._async(
            get_admin_realms_realm_clients_client_uuid_offline_sessions.asyncio,
            realm=realm,
            client_uuid=client_uuid,
            first=first,
            max_=max,
        )

    def get_client_offline_session_count(self, realm: str | None = None, *, client_uuid: str) -> int | None:
        """Get offline session count for a client (sync)."""
        return self._sync(
            get_admin_realms_realm_clients_client_uuid_offline_session_count.sync,
            realm=realm,
            client_uuid=client_uuid
        )

    async def aget_client_offline_session_count(self, realm: str | None = None, *, client_uuid: str) -> int | None:
        """Get offline session count for a client (async)."""
        return await self._async(
            get_admin_realms_realm_clients_client_uuid_offline_session_count.asyncio,
            realm=realm,
            client_uuid=client_uuid
        )

    # User session operations
    def get_user_sessions(self, realm: str | None = None, *, user_id: str) -> list | None:
        """Get sessions for a user (sync)."""
        return self._sync(
            get_admin_realms_realm_users_user_id_sessions.sync,
            realm=realm,
            user_id=user_id
        )

    async def aget_user_sessions(self, realm: str | None = None, *, user_id: str) -> list | None:
        """Get sessions for a user (async)."""
        return await self._async(
            get_admin_realms_realm_users_user_id_sessions.asyncio,
            realm=realm,
            user_id=user_id
        )

    def get_user_offline_sessions(self, realm: str | None = None, *, user_id: str, client_uuid: str) -> list | None:
        """Get offline sessions for a user and client (sync)."""
        return self._sync(
            get_admin_realms_realm_users_user_id_offline_sessions_client_uuid.sync,
            realm=realm,
            user_id=user_id,
            client_uuid=client_uuid
        )

    async def aget_user_offline_sessions(self, realm: str | None = None, *, user_id: str, client_uuid: str) -> list | None:
        """Get offline sessions for a user and client (async)."""
        return await self._async(
            get_admin_realms_realm_users_user_id_offline_sessions_client_uuid.asyncio,
            realm=realm,
            user_id=user_id,
            client_uuid=client_uuid
        )


class SessionsClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the SessionsAPI.
    """

    @cached_property
    def sessions(self) -> SessionsAPI:
        """Get the SessionsAPI instance."""
        return SessionsAPI(manager=self)  # type: ignore[arg-type]
