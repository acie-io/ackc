"""Group management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.groups import (
    get_admin_realms_realm_groups,
    post_admin_realms_realm_groups,
)
from ..generated.models import GroupRepresentation
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
        """Create a group (sync). Returns group ID."""
        group_obj = group_data if isinstance(group_data, GroupRepresentation) else GroupRepresentation.from_dict(group_data)
        response = self._sync_detailed(
            post_admin_realms_realm_groups.sync_detailed,
            realm=realm,
            body=group_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create group: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate(self, realm: str | None = None, group_data: dict | GroupRepresentation = None) -> str:
        """Create a group (async). Returns group ID."""
        group_obj = group_data if isinstance(group_data, GroupRepresentation) else GroupRepresentation.from_dict(group_data)
        response = await self._async_detailed(
            post_admin_realms_realm_groups.asyncio_detailed,
            realm=realm,
            body=group_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create group: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""


class GroupsClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the GroupsAPI.
    """

    @cached_property
    def groups(self) -> GroupsAPI:
        """Get the GroupsAPI instance."""
        return GroupsAPI(manager=self)  # type: ignore[arg-type]
