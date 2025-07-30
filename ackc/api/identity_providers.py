"""Identity provider management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.identity_providers import (
    get_admin_realms_realm_identity_provider_instances,
    post_admin_realms_realm_identity_provider_instances,
    get_admin_realms_realm_identity_provider_instances_alias,
    put_admin_realms_realm_identity_provider_instances_alias,
    delete_admin_realms_realm_identity_provider_instances_alias,
)
from ..generated.models import IdentityProviderRepresentation

__all__ = "IdentityProvidersAPI", "IdentityProvidersClientMixin", "IdentityProviderRepresentation"


class IdentityProvidersAPI(BaseAPI):
    """Identity provider management API methods."""

    def get_all(self, realm: str | None = None) -> list[IdentityProviderRepresentation] | None:
        """List identity providers in a realm (sync)."""
        return self._sync(get_admin_realms_realm_identity_provider_instances.sync, realm)

    async def aget_all(self, realm: str | None = None) -> list[IdentityProviderRepresentation] | None:
        """List identity providers in a realm (async)."""
        return await self._async(get_admin_realms_realm_identity_provider_instances.asyncio, realm)

    def create(self, realm: str | None = None, provider_data: dict | IdentityProviderRepresentation = None) -> None:
        """Create an identity provider (sync)."""
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = self._sync_detailed(
            post_admin_realms_realm_identity_provider_instances.sync_detailed,
            realm=realm,
            body=provider_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create identity provider: {response.status_code}")

    async def acreate(self, realm: str | None = None, provider_data: dict | IdentityProviderRepresentation = None) -> None:
        """Create an identity provider (async)."""
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = await self._async_detailed(
            post_admin_realms_realm_identity_provider_instances.asyncio_detailed,
            realm=realm,
            body=provider_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create identity provider: {response.status_code}")

    def get(self, realm: str | None = None, alias: str = None) -> IdentityProviderRepresentation | None:
        """Get an identity provider by alias (sync)."""
        return self._sync(
            get_admin_realms_realm_identity_provider_instances_alias.sync,
            realm=realm,
            alias=alias
        )

    async def aget(self, realm: str | None = None, alias: str = None) -> IdentityProviderRepresentation | None:
        """Get an identity provider by alias (async)."""
        return await self._async(
            get_admin_realms_realm_identity_provider_instances_alias.asyncio,
            realm=realm,
            alias=alias
        )

    def update(self, realm: str | None = None, alias: str = None, provider_data: dict | IdentityProviderRepresentation = None) -> None:
        """Update an identity provider (sync)."""
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = self._sync_detailed(
            put_admin_realms_realm_identity_provider_instances_alias.sync_detailed,
            realm=realm,
            alias=alias,
            body=provider_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update identity provider: {response.status_code}")

    async def aupdate(self, realm: str | None = None, alias: str = None, provider_data: dict | IdentityProviderRepresentation = None) -> None:
        """Update an identity provider (async)."""
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = await self._async_detailed(
            put_admin_realms_realm_identity_provider_instances_alias.asyncio_detailed,
            realm=realm,
            alias=alias,
            body=provider_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update identity provider: {response.status_code}")

    def delete(self, realm: str | None = None, alias: str = None) -> None:
        """Delete an identity provider (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_identity_provider_instances_alias.sync_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete identity provider: {response.status_code}")

    async def adelete(self, realm: str | None = None, alias: str = None) -> None:
        """Delete an identity provider (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_identity_provider_instances_alias.asyncio_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete identity provider: {response.status_code}")


class IdentityProvidersClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the IdentityProvidersAPI.
    """

    @cached_property
    def identity_providers(self) -> IdentityProvidersAPI:
        """Get the IdentityProvidersAPI instance."""
        return IdentityProvidersAPI(manager=self)  # type: ignore[arg-type]
