"""Group management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import APIError
from ..generated.api.groups import (
    get_admin_realms_realm_groups,
    get_admin_realms_realm_groups_count,
    post_admin_realms_realm_groups,
    get_admin_realms_realm_groups_group_id,
    put_admin_realms_realm_groups_group_id,
    delete_admin_realms_realm_groups_group_id,
    get_admin_realms_realm_groups_group_id_members,
    get_admin_realms_realm_groups_group_id_children,
    post_admin_realms_realm_groups_group_id_children,
    get_admin_realms_realm_groups_group_id_management_permissions,
    put_admin_realms_realm_groups_group_id_management_permissions,
)
from ..generated.models import GroupRepresentation, UserRepresentation
from ..generated.types import UNSET, Unset

__all__ = "GroupsAPI", "GroupsClientMixin", "GroupRepresentation"


class GroupsAPI(BaseAPI):
    """Group management API methods."""

    def get_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = True,
        exact: Unset | bool = False,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
        populate_hierarchy: Unset | bool = True,
        q: Unset | str = UNSET,
        search: Unset | str = UNSET,
        sub_groups_count: Unset | bool = True,
    ) -> list[GroupRepresentation] | None:
        """List groups in a realm.
        
        Args:
            realm: The realm name
            brief_representation: Only return basic group info (default True)
            exact: Exact match for searches
            first: Pagination offset
            max: Maximum results to return
            populate_hierarchy: Include full group hierarchy
            q: Query string for group search
            search: Search string (searches group name)
            sub_groups_count: Include subgroup count (default True)
            
        Returns:
            List of groups matching the filters
        """
        return self._sync(
            get_admin_realms_realm_groups.sync,
            realm,
            brief_representation=brief_representation,
            exact=exact,
            first=first,
            max_=max,
            populate_hierarchy=populate_hierarchy,
            q=q,
            search=search,
            sub_groups_count=sub_groups_count,
        )

    async def aget_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = True,
        exact: Unset | bool = False,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
        populate_hierarchy: Unset | bool = True,
        q: Unset | str = UNSET,
        search: Unset | str = UNSET,
        sub_groups_count: Unset | bool = True,
    ) -> list[GroupRepresentation] | None:
        """List groups in a realm (async).
        
        Args:
            realm: The realm name
            brief_representation: Only return basic group info (default True)
            exact: Exact match for searches
            first: Pagination offset
            max: Maximum results to return
            populate_hierarchy: Include full group hierarchy
            q: Query string for group search
            search: Search string (searches group name)
            sub_groups_count: Include subgroup count (default True)
            
        Returns:
            List of groups matching the filters
        """
        return await self._async(
            get_admin_realms_realm_groups.asyncio,
            realm,
            brief_representation=brief_representation,
            exact=exact,
            first=first,
            max_=max,
            populate_hierarchy=populate_hierarchy,
            q=q,
            search=search,
            sub_groups_count=sub_groups_count,
        )

    def create(self, realm: str | None = None, group_data: dict | GroupRepresentation = None) -> str:
        """Create a group (sync).
        
        Args:
            realm: The realm name
            group_data: Group configuration including name and path
            
        Returns:
            Created group ID
            
        Raises:
            APIError: If group creation fails
        """
        group_obj = group_data if isinstance(group_data, GroupRepresentation) else GroupRepresentation.from_dict(group_data)
        response = self._sync_detailed(
            post_admin_realms_realm_groups.sync_detailed,
            realm=realm,
            body=group_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create group: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate(self, realm: str | None = None, group_data: dict | GroupRepresentation = None) -> str:
        """Create a group (async).
        
        Args:
            realm: The realm name
            group_data: Group configuration including name and path
            
        Returns:
            Created group ID
            
        Raises:
            APIError: If group creation fails
        """
        group_obj = group_data if isinstance(group_data, GroupRepresentation) else GroupRepresentation.from_dict(group_data)
        response = await self._async_detailed(
            post_admin_realms_realm_groups.asyncio_detailed,
            realm=realm,
            body=group_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create group: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def get(self, realm: str | None = None, *, group_id: str) -> GroupRepresentation | None:
        """Get a group by ID (sync).
        
        Args:
            realm: The realm name
            group_id: Group ID
            
        Returns:
            Group representation with full details
        """
        return self._sync(
            get_admin_realms_realm_groups_group_id.sync,
            realm or self.realm,
            group_id=group_id
        )

    async def aget(self, realm: str | None = None, *, group_id: str) -> GroupRepresentation | None:
        """Get a group by ID (async).
        
        Args:
            realm: The realm name
            group_id: Group ID
            
        Returns:
            Group representation with full details
        """
        return await self._async(
            get_admin_realms_realm_groups_group_id.asyncio,
            realm or self.realm,
            group_id=group_id
        )

    def update(self, realm: str | None = None, *, group_id: str, group_data: dict | GroupRepresentation) -> None:
        """Update a group (sync).
        
        Args:
            realm: The realm name
            group_id: Group ID to update
            group_data: Updated group configuration
            
        Raises:
            APIError: If group update fails
        """
        group_obj = group_data if isinstance(group_data, GroupRepresentation) else GroupRepresentation.from_dict(group_data)
        response = self._sync_detailed(
            put_admin_realms_realm_groups_group_id.sync_detailed,
            realm or self.realm,
            group_id=group_id,
            body=group_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update group: {response.status_code}")

    async def aupdate(self, realm: str | None = None, *, group_id: str, group_data: dict | GroupRepresentation) -> None:
        """Update a group (async).
        
        Args:
            realm: The realm name
            group_id: Group ID to update
            group_data: Updated group configuration
            
        Raises:
            APIError: If group update fails
        """
        group_obj = group_data if isinstance(group_data, GroupRepresentation) else GroupRepresentation.from_dict(group_data)
        response = await self._async_detailed(
            put_admin_realms_realm_groups_group_id.asyncio_detailed,
            realm or self.realm,
            group_id=group_id,
            body=group_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update group: {response.status_code}")

    def delete(self, realm: str | None = None, *, group_id: str) -> None:
        """Delete a group (sync).
        
        Args:
            realm: The realm name
            group_id: Group ID to delete
            
        Raises:
            APIError: If group deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_groups_group_id.sync_detailed,
            realm or self.realm,
            group_id=group_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete group: {response.status_code}")

    async def adelete(self, realm: str | None = None, *, group_id: str) -> None:
        """Delete a group (async).
        
        Args:
            realm: The realm name
            group_id: Group ID to delete
            
        Raises:
            APIError: If group deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_groups_group_id.asyncio_detailed,
            realm or self.realm,
            group_id=group_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete group: {response.status_code}")

    def get_members(
        self,
        realm: str | None = None,
        *,
        group_id: str,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
    ) -> list[UserRepresentation] | None:
        """Get group members (sync).
        
        Args:
            realm: The realm name
            group_id: Group ID
            first: Pagination offset
            max: Maximum results to return
            
        Returns:
            List of users who are members of the group
        """
        return self._sync(
            get_admin_realms_realm_groups_group_id_members.sync,
            realm or self.realm,
            group_id=group_id,
            first=first,
            max_=max,
        )

    async def aget_members(
        self,
        realm: str | None = None,
        *,
        group_id: str,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
    ) -> list[UserRepresentation] | None:
        """Get group members (async).
        
        Args:
            realm: The realm name
            group_id: Group ID
            first: Pagination offset
            max: Maximum results to return
            
        Returns:
            List of users who are members of the group
        """
        return await self._async(
            get_admin_realms_realm_groups_group_id_members.asyncio,
            realm or self.realm,
            group_id=group_id,
            first=first,
            max_=max,
        )

    def get_count(self, realm: str | None = None, *, search: str | None = None, top: bool = False) -> int | None:
        """Get total group count (sync).
        
        Args:
            realm: The realm name
            search: Optional search string to filter groups
            top: If True, only count top-level groups
            
        Returns:
            Total number of groups matching criteria
        """
        params = {}
        if search:
            params["search"] = search
        if top:
            params["top"] = top
        result = self._sync(
            get_admin_realms_realm_groups_count.sync,
            realm or self.realm,
            **params
        )
        if result and hasattr(result, 'additional_properties'):
            return result.additional_properties.get("count")
        return result["count"] if result and "count" in result else None

    async def aget_count(self, realm: str | None = None, *, search: str | None = None, top: bool = False) -> int | None:
        """Get total group count (async).
        
        Args:
            realm: The realm name
            search: Optional search string to filter groups
            top: If True, only count top-level groups
            
        Returns:
            Total number of groups matching criteria
        """
        params = {}
        if search:
            params["search"] = search
        if top:
            params["top"] = top
        result = await self._async(
            get_admin_realms_realm_groups_count.asyncio,
            realm or self.realm,
            **params
        )
        if result and hasattr(result, 'additional_properties'):
            return result.additional_properties.get("count")
        return result["count"] if result and "count" in result else None

    def get_children(self, realm: str | None = None, *, group_id: str, first: int | None = None, max_results: int | None = None) -> list[GroupRepresentation] | None:
        """Get child groups (sync).
        
        Args:
            realm: The realm name
            group_id: Parent group ID
            first: Pagination offset
            max_results: Maximum results to return
            
        Returns:
            List of child groups
        """
        params = {}
        if first is not None:
            params["first"] = first
        if max_results is not None:
            params["max_"] = max_results
        return self._sync(
            get_admin_realms_realm_groups_group_id_children.sync,
            realm or self.realm,
            group_id=group_id,
            **params
        )

    async def aget_children(self, realm: str | None = None, *, group_id: str, first: int | None = None, max_results: int | None = None) -> list[GroupRepresentation] | None:
        """Get child groups (async).
        
        Args:
            realm: The realm name
            group_id: Parent group ID
            first: Pagination offset
            max_results: Maximum results to return
            
        Returns:
            List of child groups
        """
        params = {}
        if first is not None:
            params["first"] = first
        if max_results is not None:
            params["max_"] = max_results
        return await self._async(
            get_admin_realms_realm_groups_group_id_children.asyncio,
            realm or self.realm,
            group_id=group_id,
            **params
        )

    def add_child(self, realm: str | None = None, *, group_id: str, child_data: dict | GroupRepresentation) -> str:
        """Add a child group (sync).
        
        Creates a new group as a child of the specified parent group.
        
        Args:
            realm: The realm name
            group_id: Parent group ID
            child_data: Child group configuration
            
        Returns:
            Created child group ID
            
        Raises:
            APIError: If child group creation fails
        """
        group_obj = child_data if isinstance(child_data, GroupRepresentation) else GroupRepresentation.from_dict(child_data)
        response = self._sync_detailed(
            post_admin_realms_realm_groups_group_id_children.sync_detailed,
            realm or self.realm,
            group_id=group_id,
            body=group_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add child group: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def aadd_child(self, realm: str | None = None, *, group_id: str, child_data: dict | GroupRepresentation) -> str:
        """Add a child group (async).
        
        Creates a new group as a child of the specified parent group.
        
        Args:
            realm: The realm name
            group_id: Parent group ID
            child_data: Child group configuration
            
        Returns:
            Created child group ID
            
        Raises:
            APIError: If child group creation fails
        """
        group_obj = child_data if isinstance(child_data, GroupRepresentation) else GroupRepresentation.from_dict(child_data)
        response = await self._async_detailed(
            post_admin_realms_realm_groups_group_id_children.asyncio_detailed,
            realm or self.realm,
            group_id=group_id,
            body=group_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add child group: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""


class GroupsClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the GroupsAPI.
    """

    @cached_property
    def groups(self) -> GroupsAPI:
        """Get the GroupsAPI instance."""
        return GroupsAPI(manager=self)  # type: ignore[arg-type]
