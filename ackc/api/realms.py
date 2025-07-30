"""Realm management API methods."""
import json
from functools import cached_property
from io import BytesIO

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.realms_admin import (
    get_admin_realms,
    post_admin_realms,
    get_admin_realms_realm,
    put_admin_realms_realm,
    delete_admin_realms_realm,
)
from ..generated.models import RealmRepresentation
from ..generated.types import File

__all__ = "RealmsAPI", "RealmsClientMixin", "RealmRepresentation"


class RealmsAPI(BaseAPI):
    """Realm management API methods."""

    def get_all(self) -> list | None:
        """List all realms (sync)."""
        return self._sync_any(get_admin_realms.sync)

    async def aget_all(self) -> list | None:
        """List all realms (async)."""
        return await self._async_any(get_admin_realms.asyncio)

    def create(self, realm_data: dict | RealmRepresentation) -> None:
        """Create a realm (sync)."""
        if isinstance(realm_data, RealmRepresentation):
            realm_dict = realm_data.to_dict()
        else:
            realm_dict = realm_data

        json_bytes = json.dumps(realm_dict).encode('utf-8')
        file_obj = File(
            payload=BytesIO(json_bytes),
            file_name="realm.json",
            mime_type="application/json"
        )

        response = self._sync_any(post_admin_realms.sync_detailed, body=file_obj)
        if response.status_code != 201:
            raise AuthError(f"Failed to create realm: {response.status_code}")

    async def acreate(self, realm_data: dict | RealmRepresentation) -> None:
        """Create a realm (async)."""
        if isinstance(realm_data, RealmRepresentation):
            realm_dict = realm_data.to_dict()
        else:
            realm_dict = realm_data

        json_bytes = json.dumps(realm_dict).encode('utf-8')
        file_obj = File(
            payload=BytesIO(json_bytes),
            file_name="realm.json",
            mime_type="application/json"
        )

        response = await self._async_any(post_admin_realms.asyncio_detailed, body=file_obj)
        if response.status_code != 201:
            raise AuthError(f"Failed to create realm: {response.status_code}")

    def get(self, realm: str) -> dict | None:
        """Get a realm (sync)."""
        return self._sync_any(get_admin_realms_realm.sync, realm=realm)

    async def aget(self, realm: str) -> dict | None:
        """Get a realm (async)."""
        return await self._async_any(get_admin_realms_realm.asyncio, realm=realm)

    def update(self, realm: str, realm_data: dict | RealmRepresentation) -> None:
        """Update a realm (sync)."""
        realm_obj = realm_data if isinstance(realm_data, RealmRepresentation) else RealmRepresentation.from_dict(
            realm_data)
        response = self._sync_any(put_admin_realms_realm.sync_detailed, realm=realm, body=realm_obj)
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update realm: {response.status_code}")

    async def aupdate(self, realm: str, realm_data: dict | RealmRepresentation) -> None:
        """Update a realm (async)."""
        realm_obj = realm_data if isinstance(realm_data, RealmRepresentation) else RealmRepresentation.from_dict(
            realm_data)
        response = await self._async_any(put_admin_realms_realm.asyncio_detailed, realm=realm, body=realm_obj)
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update realm: {response.status_code}")

    def delete(self, realm: str) -> None:
        """Delete a realm (sync)."""
        response = self._sync_any(delete_admin_realms_realm.sync_detailed, realm=realm)
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete realm: {response.status_code}")

    async def adelete(self, realm: str) -> None:
        """Delete a realm (async)."""
        response = await self._async_any(delete_admin_realms_realm.asyncio_detailed, realm=realm)
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete realm: {response.status_code}")


class RealmsClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the RealmsAPI.
    """

    @cached_property
    def realms(self) -> RealmsAPI:
        """Get the RealmsAPI instance."""
        return RealmsAPI(manager=self)  # type: ignore[arg-type]
