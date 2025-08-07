"""Identity provider management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import APIError
from ..generated.api.identity_providers import (
    get_admin_realms_realm_identity_provider_instances,
    post_admin_realms_realm_identity_provider_instances,
    get_admin_realms_realm_identity_provider_instances_alias,
    put_admin_realms_realm_identity_provider_instances_alias,
    delete_admin_realms_realm_identity_provider_instances_alias,
    get_admin_realms_realm_identity_provider_instances_alias_mappers,
    post_admin_realms_realm_identity_provider_instances_alias_mappers,
    get_admin_realms_realm_identity_provider_instances_alias_mappers_id,
    put_admin_realms_realm_identity_provider_instances_alias_mappers_id,
    delete_admin_realms_realm_identity_provider_instances_alias_mappers_id,
    get_admin_realms_realm_identity_provider_instances_alias_mapper_types,
    get_admin_realms_realm_identity_provider_instances_alias_export,
    post_admin_realms_realm_identity_provider_import_config,
)
from ..generated.models import IdentityProviderRepresentation, IdentityProviderMapperRepresentation

__all__ = "IdentityProvidersAPI", "IdentityProvidersClientMixin", "IdentityProviderRepresentation"


class IdentityProvidersAPI(BaseAPI):
    """Identity provider management API methods."""

    def get_all(self, realm: str | None = None) -> list[IdentityProviderRepresentation] | None:
        """List identity providers in a realm (sync).
        
        Args:
            realm: The realm name
            
        Returns:
            List of configured identity providers (Google, SAML, OIDC, etc.)
        """
        return self._sync(get_admin_realms_realm_identity_provider_instances.sync, realm)

    async def aget_all(self, realm: str | None = None) -> list[IdentityProviderRepresentation] | None:
        """List identity providers in a realm (async).
        
        Args:
            realm: The realm name
            
        Returns:
            List of configured identity providers (Google, SAML, OIDC, etc.)
        """
        return await self._async(get_admin_realms_realm_identity_provider_instances.asyncio, realm)

    def create(self, realm: str | None = None, *, provider_data: dict | IdentityProviderRepresentation) -> None:
        """Create an identity provider (sync).
        
        Args:
            realm: The realm name
            provider_data: Identity provider configuration
            
        Raises:
            APIError: If creation fails
        """
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = self._sync_detailed(
            post_admin_realms_realm_identity_provider_instances.sync_detailed,
            realm=realm,
            body=provider_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create identity provider: {response.status_code}")

    async def acreate(self, realm: str | None = None, *, provider_data: dict | IdentityProviderRepresentation) -> None:
        """Create an identity provider (async).
        
        Args:
            realm: The realm name
            provider_data: Identity provider configuration
            
        Raises:
            APIError: If creation fails
        """
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = await self._async_detailed(
            post_admin_realms_realm_identity_provider_instances.asyncio_detailed,
            realm=realm,
            body=provider_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create identity provider: {response.status_code}")

    def get(self, realm: str | None = None, *, alias: str) -> IdentityProviderRepresentation | None:
        """Get an identity provider by alias (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            
        Returns:
            Identity provider configuration
        """
        return self._sync(
            get_admin_realms_realm_identity_provider_instances_alias.sync,
            realm=realm,
            alias=alias
        )

    async def aget(self, realm: str | None = None, *, alias: str) -> IdentityProviderRepresentation | None:
        """Get an identity provider by alias (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            
        Returns:
            Identity provider configuration
        """
        return await self._async(
            get_admin_realms_realm_identity_provider_instances_alias.asyncio,
            realm=realm,
            alias=alias
        )

    def update(self, realm: str | None = None, *, alias: str, provider_data: dict | IdentityProviderRepresentation) -> None:
        """Update an identity provider (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            provider_data: Updated provider configuration
            
        Raises:
            APIError: If update fails
        """
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = self._sync_detailed(
            put_admin_realms_realm_identity_provider_instances_alias.sync_detailed,
            realm=realm,
            alias=alias,
            body=provider_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update identity provider: {response.status_code}")

    async def aupdate(self, realm: str | None = None, *, alias: str, provider_data: dict | IdentityProviderRepresentation) -> None:
        """Update an identity provider (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            provider_data: Updated provider configuration
            
        Raises:
            APIError: If update fails
        """
        provider_obj = provider_data if isinstance(provider_data, IdentityProviderRepresentation) else IdentityProviderRepresentation.from_dict(provider_data)
        response = await self._async_detailed(
            put_admin_realms_realm_identity_provider_instances_alias.asyncio_detailed,
            realm=realm,
            alias=alias,
            body=provider_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update identity provider: {response.status_code}")

    def delete(self, realm: str | None = None, *, alias: str) -> None:
        """Delete an identity provider (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias to delete
            
        Raises:
            APIError: If deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_identity_provider_instances_alias.sync_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete identity provider: {response.status_code}")

    async def adelete(self, realm: str | None = None, *, alias: str) -> None:
        """Delete an identity provider (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias to delete
            
        Raises:
            APIError: If deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_identity_provider_instances_alias.asyncio_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete identity provider: {response.status_code}")

    def get_mappers(self, realm: str | None = None, *, alias: str) -> list[IdentityProviderMapperRepresentation] | None:
        """Get identity provider mappers (sync).
        
        Mappers define how external identity provider data maps to Keycloak user attributes.
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            
        Returns:
            List of configured mappers for the identity provider
        """
        return self._sync(
            get_admin_realms_realm_identity_provider_instances_alias_mappers.sync,
            realm or self.realm,
            alias=alias
        )

    async def aget_mappers(self, realm: str | None = None, *, alias: str) -> list[IdentityProviderMapperRepresentation] | None:
        """Get identity provider mappers (async).
        
        Mappers define how external identity provider data maps to Keycloak user attributes.
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            
        Returns:
            List of configured mappers for the identity provider
        """
        return await self._async(
            get_admin_realms_realm_identity_provider_instances_alias_mappers.asyncio,
            realm or self.realm,
            alias=alias
        )

    def create_mapper(
        self,
        realm: str | None = None,
        *,
        alias: str,
        mapper_data: dict | IdentityProviderMapperRepresentation
    ) -> str:
        """Create identity provider mapper (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_data: Mapper configuration
            
        Returns:
            Created mapper ID
            
        Raises:
            APIError: If mapper creation fails
        """
        mapper_obj = (
            mapper_data if isinstance(mapper_data, IdentityProviderMapperRepresentation)
            else IdentityProviderMapperRepresentation.from_dict(mapper_data)
        )
        response = self._sync_detailed(
            post_admin_realms_realm_identity_provider_instances_alias_mappers.sync_detailed,
            realm or self.realm,
            alias=alias,
            body=mapper_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create mapper: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate_mapper(
        self,
        realm: str | None = None,
        *,
        alias: str,
        mapper_data: dict | IdentityProviderMapperRepresentation
    ) -> str:
        """Create identity provider mapper (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_data: Mapper configuration
            
        Returns:
            Created mapper ID
            
        Raises:
            APIError: If mapper creation fails
        """
        mapper_obj = (
            mapper_data if isinstance(mapper_data, IdentityProviderMapperRepresentation)
            else IdentityProviderMapperRepresentation.from_dict(mapper_data)
        )
        response = await self._async_detailed(
            post_admin_realms_realm_identity_provider_instances_alias_mappers.asyncio_detailed,
            realm or self.realm,
            alias=alias,
            body=mapper_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create mapper: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def get_mapper(self, realm: str | None = None, *, alias: str, mapper_id: str) -> IdentityProviderMapperRepresentation | None:
        """Get identity provider mapper (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_id: Mapper ID
            
        Returns:
            Mapper configuration
        """
        return self._sync(
            get_admin_realms_realm_identity_provider_instances_alias_mappers_id.sync,
            realm or self.realm,
            alias=alias,
            id=mapper_id
        )

    async def aget_mapper(self, realm: str | None = None, *, alias: str, mapper_id: str) -> IdentityProviderMapperRepresentation | None:
        """Get identity provider mapper (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_id: Mapper ID
            
        Returns:
            Mapper configuration
        """
        return await self._async(
            get_admin_realms_realm_identity_provider_instances_alias_mappers_id.asyncio,
            realm or self.realm,
            alias=alias,
            id=mapper_id
        )

    def update_mapper(
        self,
        realm: str | None = None,
        *,
        alias: str,
        mapper_id: str,
        mapper_data: dict | IdentityProviderMapperRepresentation
    ) -> None:
        """Update identity provider mapper (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_id: Mapper ID to update
            mapper_data: Updated mapper configuration
            
        Raises:
            APIError: If mapper update fails
        """
        mapper_obj = (
            mapper_data if isinstance(mapper_data, IdentityProviderMapperRepresentation)
            else IdentityProviderMapperRepresentation.from_dict(mapper_data)
        )
        response = self._sync_detailed(
            put_admin_realms_realm_identity_provider_instances_alias_mappers_id.sync_detailed,
            realm or self.realm,
            alias=alias,
            id=mapper_id,
            body=mapper_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update mapper: {response.status_code}")

    async def aupdate_mapper(
        self,
        realm: str | None = None,
        *,
        alias: str,
        mapper_id: str,
        mapper_data: dict | IdentityProviderMapperRepresentation
    ) -> None:
        """Update identity provider mapper (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_id: Mapper ID to update
            mapper_data: Updated mapper configuration
            
        Raises:
            APIError: If mapper update fails
        """
        mapper_obj = (
            mapper_data if isinstance(mapper_data, IdentityProviderMapperRepresentation)
            else IdentityProviderMapperRepresentation.from_dict(mapper_data)
        )
        response = await self._async_detailed(
            put_admin_realms_realm_identity_provider_instances_alias_mappers_id.asyncio_detailed,
            realm or self.realm,
            alias=alias,
            id=mapper_id,
            body=mapper_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update mapper: {response.status_code}")

    def delete_mapper(self, realm: str | None = None, *, alias: str, mapper_id: str) -> None:
        """Delete identity provider mapper (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_id: Mapper ID to delete
            
        Raises:
            APIError: If mapper deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_identity_provider_instances_alias_mappers_id.sync_detailed,
            realm or self.realm,
            alias=alias,
            id=mapper_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete mapper: {response.status_code}")

    async def adelete_mapper(self, realm: str | None = None, *, alias: str, mapper_id: str) -> None:
        """Delete identity provider mapper (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            mapper_id: Mapper ID to delete
            
        Raises:
            APIError: If mapper deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_identity_provider_instances_alias_mappers_id.asyncio_detailed,
            realm or self.realm,
            alias=alias,
            id=mapper_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete mapper: {response.status_code}")

    def get_mapper_types(self, realm: str | None = None, *, alias: str) -> dict | None:
        """Get available mapper types (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            
        Returns:
            Dictionary of available mapper types and their configurations
        """
        return self._sync(
            get_admin_realms_realm_identity_provider_instances_alias_mapper_types.sync,
            realm or self.realm,
            alias=alias
        )

    async def aget_mapper_types(self, realm: str | None = None, *, alias: str) -> dict | None:
        """Get available mapper types (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            
        Returns:
            Dictionary of available mapper types and their configurations
        """
        return await self._async(
            get_admin_realms_realm_identity_provider_instances_alias_mapper_types.asyncio,
            realm or self.realm,
            alias=alias
        )

    def export(self, realm: str | None = None, *, alias: str, format: str | None = None) -> dict | None:
        """Export identity provider configuration (sync).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            format: Export format (e.g., 'json', 'saml-metadata')
            
        Returns:
            Exported configuration in requested format
        """
        params = {}
        if format:
            params["format"] = format
        return self._sync(
            get_admin_realms_realm_identity_provider_instances_alias_export.sync,
            realm or self.realm,
            alias=alias,
            **params
        )

    async def aexport(self, realm: str | None = None, *, alias: str, format: str | None = None) -> dict | None:
        """Export identity provider configuration (async).
        
        Args:
            realm: The realm name
            alias: Identity provider alias
            format: Export format (e.g., 'json', 'saml-metadata')
            
        Returns:
            Exported configuration in requested format
        """
        params = {}
        if format:
            params["format"] = format
        return await self._async(
            get_admin_realms_realm_identity_provider_instances_alias_export.asyncio,
            realm or self.realm,
            alias=alias,
            **params
        )

    def import_config(self, realm: str | None = None, *, data: dict) -> dict[str, str] | None:
        """Import identity provider from configuration (sync).
        
        Args:
            realm: The realm name
            data: Identity provider configuration to import
            
        Returns:
            Import result with created provider details
        """
        result = self._sync(
            post_admin_realms_realm_identity_provider_import_config.sync,
            realm or self.realm,
            body=data
        )
        if result and hasattr(result, 'additional_properties'):
            return result.additional_properties
        return result

    async def aimport_config(self, realm: str | None = None, *, data: dict) -> dict[str, str] | None:
        """Import identity provider from configuration (async).
        
        Args:
            realm: The realm name
            data: Identity provider configuration to import
            
        Returns:
            Import result with created provider details
        """
        result = await self._async(
            post_admin_realms_realm_identity_provider_import_config.asyncio,
            realm or self.realm,
            body=data
        )
        if result and hasattr(result, 'additional_properties'):
            return result.additional_properties
        return result


class IdentityProvidersClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the IdentityProvidersAPI.
    """

    @cached_property
    def identity_providers(self) -> IdentityProvidersAPI:
        """Get the IdentityProvidersAPI instance."""
        return IdentityProvidersAPI(manager=self)  # type: ignore[arg-type]
