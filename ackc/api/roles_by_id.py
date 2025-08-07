"""Roles by ID API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import APIError
from ..generated.api.roles_by_id import (
    get_admin_realms_realm_roles_by_id_role_id,
    put_admin_realms_realm_roles_by_id_role_id,
    delete_admin_realms_realm_roles_by_id_role_id,
    get_admin_realms_realm_roles_by_id_role_id_composites,
    get_admin_realms_realm_roles_by_id_role_id_composites_realm,
    get_admin_realms_realm_roles_by_id_role_id_composites_clients_client_uuid,
    post_admin_realms_realm_roles_by_id_role_id_composites,
    delete_admin_realms_realm_roles_by_id_role_id_composites,
    get_admin_realms_realm_roles_by_id_role_id_management_permissions,
    put_admin_realms_realm_roles_by_id_role_id_management_permissions,
)
from ..generated.models import RoleRepresentation, ManagementPermissionReference

__all__ = "RolesByIdAPI", "RolesByIdClientMixin"


class RolesByIdAPI(BaseAPI):
    """Roles by ID API methods."""

    def get(self, realm: str | None = None, *, role_id: str) -> RoleRepresentation | None:
        """Get a role by ID (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            Role representation with full details
        """
        return self._sync(
            get_admin_realms_realm_roles_by_id_role_id.sync,
            realm or self.realm,
            role_id=role_id
        )

    async def aget(self, realm: str | None = None, *, role_id: str) -> RoleRepresentation | None:
        """Get a role by ID (async).
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            Role representation with full details
        """
        return await self._async(
            get_admin_realms_realm_roles_by_id_role_id.asyncio,
            realm or self.realm,
            role_id=role_id
        )

    def update(self, realm: str | None = None, *, role_id: str, role_data: dict | RoleRepresentation) -> None:
        """Update a role by ID (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID to update
            role_data: Updated role configuration
            
        Raises:
            APIError: If role update fails
        """
        role_obj = role_data if isinstance(role_data, RoleRepresentation) else RoleRepresentation.from_dict(role_data)
        response = self._sync_detailed(
            put_admin_realms_realm_roles_by_id_role_id.sync_detailed,
            realm or self.realm,
            role_id=role_id,
            body=role_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update role: {response.status_code}")

    async def aupdate(self, realm: str | None = None, *, role_id: str, role_data: dict | RoleRepresentation) -> None:
        """Update a role by ID (async).
        
        Args:
            realm: The realm name
            role_id: Role ID to update
            role_data: Updated role configuration
            
        Raises:
            APIError: If role update fails
        """
        role_obj = role_data if isinstance(role_data, RoleRepresentation) else RoleRepresentation.from_dict(role_data)
        response = await self._async_detailed(
            put_admin_realms_realm_roles_by_id_role_id.asyncio_detailed,
            realm or self.realm,
            role_id=role_id,
            body=role_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update role: {response.status_code}")

    def delete(self, realm: str | None = None, *, role_id: str) -> None:
        """Delete a role by ID (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID to delete
            
        Raises:
            APIError: If role deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_roles_by_id_role_id.sync_detailed,
            realm or self.realm,
            role_id=role_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete role: {response.status_code}")

    async def adelete(self, realm: str | None = None, *, role_id: str) -> None:
        """Delete a role by ID (async).
        
        Args:
            realm: The realm name
            role_id: Role ID to delete
            
        Raises:
            APIError: If role deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_roles_by_id_role_id.asyncio_detailed,
            realm or self.realm,
            role_id=role_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete role: {response.status_code}")

    def get_composites(self, realm: str | None = None, *, role_id: str) -> list[RoleRepresentation] | None:
        """Get composite roles for a role (sync).
        
        Composite roles combine permissions from multiple roles.
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            List of composite roles that make up this role
        """
        return self._sync(
            get_admin_realms_realm_roles_by_id_role_id_composites.sync,
            realm or self.realm,
            role_id=role_id
        )

    async def aget_composites(self, realm: str | None = None, *, role_id: str) -> list[RoleRepresentation] | None:
        """Get composite roles for a role (async).
        
        Composite roles combine permissions from multiple roles.
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            List of composite roles that make up this role
        """
        return await self._async(
            get_admin_realms_realm_roles_by_id_role_id_composites.asyncio,
            realm or self.realm,
            role_id=role_id
        )

    def get_realm_composites(self, realm: str | None = None, *, role_id: str) -> list[RoleRepresentation] | None:
        """Get realm-level composite roles for a role (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            List of realm-level composite roles
        """
        return self._sync(
            get_admin_realms_realm_roles_by_id_role_id_composites_realm.sync,
            realm or self.realm,
            role_id=role_id
        )

    async def aget_realm_composites(self, realm: str | None = None, *, role_id: str) -> list[RoleRepresentation] | None:
        """Get realm-level composite roles for a role (async).
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            List of realm-level composite roles
        """
        return await self._async(
            get_admin_realms_realm_roles_by_id_role_id_composites_realm.asyncio,
            realm or self.realm,
            role_id=role_id
        )

    def get_client_composites(self, realm: str | None = None, *, role_id: str, client_uuid: str) -> list[RoleRepresentation] | None:
        """Get client-level composite roles for a role (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID
            client_uuid: Client UUID
            
        Returns:
            List of client-level composite roles
        """
        return self._sync(
            get_admin_realms_realm_roles_by_id_role_id_composites_clients_client_uuid.sync,
            realm or self.realm,
            role_id=role_id,
            client_uuid=client_uuid
        )

    async def aget_client_composites(self, realm: str | None = None, *, role_id: str, client_uuid: str) -> list[RoleRepresentation] | None:
        """Get client-level composite roles for a role (async).
        
        Args:
            realm: The realm name
            role_id: Role ID
            client_uuid: Client UUID
            
        Returns:
            List of client-level composite roles
        """
        return await self._async(
            get_admin_realms_realm_roles_by_id_role_id_composites_clients_client_uuid.asyncio,
            realm or self.realm,
            role_id=role_id,
            client_uuid=client_uuid
        )

    def add_composites(self, realm: str | None = None, *, role_id: str, roles: list[RoleRepresentation]) -> None:
        """Add composite roles to a role (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID
            roles: List of roles to add as composites
            
        Raises:
            APIError: If adding composite roles fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_roles_by_id_role_id_composites.sync_detailed,
            realm or self.realm,
            role_id=role_id,
            body=roles
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to add composite roles: {response.status_code}")

    async def aadd_composites(self, realm: str | None = None, *, role_id: str, roles: list[RoleRepresentation]) -> None:
        """Add composite roles to a role (async).
        
        Args:
            realm: The realm name
            role_id: Role ID
            roles: List of roles to add as composites
            
        Raises:
            APIError: If adding composite roles fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_roles_by_id_role_id_composites.asyncio_detailed,
            realm or self.realm,
            role_id=role_id,
            body=roles
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to add composite roles: {response.status_code}")

    def remove_composites(self, realm: str | None = None, *, role_id: str, roles: list[RoleRepresentation]) -> None:
        """Remove composite roles from a role (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID
            roles: List of roles to remove from composites
            
        Raises:
            APIError: If removing composite roles fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_roles_by_id_role_id_composites.sync_detailed,
            realm or self.realm,
            role_id=role_id,
            body=roles
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to remove composite roles: {response.status_code}")

    async def aremove_composites(self, realm: str | None = None, *, role_id: str, roles: list[RoleRepresentation]) -> None:
        """Remove composite roles from a role (async).
        
        Args:
            realm: The realm name
            role_id: Role ID
            roles: List of roles to remove from composites
            
        Raises:
            APIError: If removing composite roles fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_roles_by_id_role_id_composites.asyncio_detailed,
            realm or self.realm,
            role_id=role_id,
            body=roles
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to remove composite roles: {response.status_code}")

    def get_management_permissions(self, realm: str | None = None, *, role_id: str) -> ManagementPermissionReference | None:
        """Get management permissions for a role (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            Management permission reference with enabled status and resource information
        """
        return self._sync(
            get_admin_realms_realm_roles_by_id_role_id_management_permissions.sync,
            realm or self.realm,
            role_id=role_id
        )

    async def aget_management_permissions(self, realm: str | None = None, *, role_id: str) -> ManagementPermissionReference | None:
        """Get management permissions for a role (async).
        
        Args:
            realm: The realm name
            role_id: Role ID
            
        Returns:
            Management permission reference with enabled status and resource information
        """
        return await self._async(
            get_admin_realms_realm_roles_by_id_role_id_management_permissions.asyncio,
            realm or self.realm,
            role_id=role_id
        )

    def update_management_permissions(self, realm: str | None = None, *, role_id: str, ref: dict | ManagementPermissionReference) -> ManagementPermissionReference | None:
        """Update management permissions for a role (sync).
        
        Args:
            realm: The realm name
            role_id: Role ID
            ref: Management permission reference to update
            
        Returns:
            Updated management permission reference
        """
        ref_obj = ref if isinstance(ref, ManagementPermissionReference) else ManagementPermissionReference.from_dict(ref)
        return self._sync(
            put_admin_realms_realm_roles_by_id_role_id_management_permissions.sync,
            realm or self.realm,
            role_id=role_id,
            body=ref_obj
        )

    async def aupdate_management_permissions(self, realm: str | None = None, *, role_id: str, ref: dict | ManagementPermissionReference) -> ManagementPermissionReference | None:
        """Update management permissions for a role (async).
        
        Args:
            realm: The realm name
            role_id: Role ID
            ref: Management permission reference to update
            
        Returns:
            Updated management permission reference
        """
        ref_obj = ref if isinstance(ref, ManagementPermissionReference) else ManagementPermissionReference.from_dict(ref)
        return await self._async(
            put_admin_realms_realm_roles_by_id_role_id_management_permissions.asyncio,
            realm or self.realm,
            role_id=role_id,
            body=ref_obj
        )


class RolesByIdClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the RolesByIdAPI."""
    
    @cached_property
    def roles_by_id(self) -> RolesByIdAPI:
        """Get the RolesByIdAPI instance."""
        return RolesByIdAPI(manager=self)  # type: ignore[arg-type]