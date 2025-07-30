"""Authentication management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..generated.api.authentication_management import (
    # Flows
    get_admin_realms_realm_authentication_flows,
    post_admin_realms_realm_authentication_flows,
    get_admin_realms_realm_authentication_flows_id,
    put_admin_realms_realm_authentication_flows_id,
    delete_admin_realms_realm_authentication_flows_id,
    post_admin_realms_realm_authentication_flows_flow_alias_copy,
    # Executions
    get_admin_realms_realm_authentication_flows_flow_alias_executions,
    put_admin_realms_realm_authentication_flows_flow_alias_executions,
    post_admin_realms_realm_authentication_flows_flow_alias_executions_execution,
    post_admin_realms_realm_authentication_flows_flow_alias_executions_flow,
    get_admin_realms_realm_authentication_executions_execution_id,
    delete_admin_realms_realm_authentication_executions_execution_id,
    post_admin_realms_realm_authentication_executions_execution_id_config,
    post_admin_realms_realm_authentication_executions_execution_id_lower_priority,
    post_admin_realms_realm_authentication_executions_execution_id_raise_priority,
    # Configs
    get_admin_realms_realm_authentication_config_id,
    put_admin_realms_realm_authentication_config_id,
    delete_admin_realms_realm_authentication_config_id,
    post_admin_realms_realm_authentication_config,
    # Providers
    get_admin_realms_realm_authentication_authenticator_providers,
    get_admin_realms_realm_authentication_client_authenticator_providers,
    get_admin_realms_realm_authentication_form_action_providers,
    get_admin_realms_realm_authentication_form_providers,
    # Required Actions
    get_admin_realms_realm_authentication_required_actions,
    get_admin_realms_realm_authentication_required_actions_alias,
    put_admin_realms_realm_authentication_required_actions_alias,
    delete_admin_realms_realm_authentication_required_actions_alias,
    post_admin_realms_realm_authentication_required_actions_alias_lower_priority,
    post_admin_realms_realm_authentication_required_actions_alias_raise_priority,
    get_admin_realms_realm_authentication_unregistered_required_actions,
    post_admin_realms_realm_authentication_register_required_action,
)
from ..generated.models import (
    AuthenticationFlowRepresentation,
    AuthenticationExecutionInfoRepresentation,
    AuthenticatorConfigRepresentation,
    RequiredActionProviderRepresentation,
)
from ..exceptions import AuthError

__all__ = (
    "AuthenticationAPI", 
    "AuthenticationClientMixin",
    "AuthenticationFlowRepresentation",
    "AuthenticationExecutionInfoRepresentation",
    "AuthenticatorConfigRepresentation",
    "RequiredActionProviderRepresentation",
)


class AuthenticationAPI(BaseAPI):
    """Authentication management API methods."""

    # Authentication Flows
    def get_flows(self, realm: str | None = None) -> list[AuthenticationFlowRepresentation] | None:
        """Get authentication flows (sync)."""
        return self._sync(get_admin_realms_realm_authentication_flows.sync, realm)

    async def aget_flows(self, realm: str | None = None) -> list[AuthenticationFlowRepresentation] | None:
        """Get authentication flows (async)."""
        return await self._async(get_admin_realms_realm_authentication_flows.asyncio, realm)

    def create_flow(self, realm: str | None = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Create an authentication flow (sync)."""
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_flows.sync_detailed,
            realm=realm,
            body=flow_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create flow: {response.status_code}")

    async def acreate_flow(self, realm: str | None = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Create an authentication flow (async)."""
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_flows.asyncio_detailed,
            realm=realm,
            body=flow_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create flow: {response.status_code}")

    def get_flow(self, realm: str | None = None, flow_id: str = None) -> AuthenticationFlowRepresentation | None:
        """Get an authentication flow by ID (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_flows_id.sync,
            realm=realm,
            id=flow_id
        )

    async def aget_flow(self, realm: str | None = None, flow_id: str = None) -> AuthenticationFlowRepresentation | None:
        """Get an authentication flow by ID (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_flows_id.asyncio,
            realm=realm,
            id=flow_id
        )

    def update_flow(self, realm: str | None = None, flow_id: str = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Update an authentication flow (sync)."""
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_flows_id.sync_detailed,
            realm=realm,
            id=flow_id,
            body=flow_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update flow: {response.status_code}")

    async def aupdate_flow(self, realm: str | None = None, flow_id: str = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Update an authentication flow (async)."""
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_flows_id.asyncio_detailed,
            realm=realm,
            id=flow_id,
            body=flow_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update flow: {response.status_code}")

    def delete_flow(self, realm: str | None = None, flow_id: str = None) -> None:
        """Delete an authentication flow (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_authentication_flows_id.sync_detailed,
            realm=realm,
            id=flow_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete flow: {response.status_code}")

    async def adelete_flow(self, realm: str | None = None, flow_id: str = None) -> None:
        """Delete an authentication flow (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_authentication_flows_id.asyncio_detailed,
            realm=realm,
            id=flow_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete flow: {response.status_code}")

    def copy_flow(self, realm: str | None = None, flow_alias: str = None, new_name: str = None) -> None:
        """Copy an authentication flow (sync)."""
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_copy.sync_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body={"newName": new_name}
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to copy flow: {response.status_code}")

    async def acopy_flow(self, realm: str | None = None, flow_alias: str = None, new_name: str = None) -> None:
        """Copy an authentication flow (async)."""
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_copy.asyncio_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body={"newName": new_name}
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to copy flow: {response.status_code}")

    # Flow Executions
    def get_executions(self, realm: str | None = None, flow_alias: str = None) -> list[AuthenticationExecutionInfoRepresentation] | None:
        """Get executions for a flow (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_flows_flow_alias_executions.sync,
            realm=realm,
            flow_alias=flow_alias
        )

    async def aget_executions(self, realm: str | None = None, flow_alias: str = None) -> list[AuthenticationExecutionInfoRepresentation] | None:
        """Get executions for a flow (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_flows_flow_alias_executions.asyncio,
            realm=realm,
            flow_alias=flow_alias
        )

    def update_executions(self, realm: str | None = None, flow_alias: str = None, execution_data: AuthenticationExecutionInfoRepresentation = None) -> None:
        """Update executions for a flow (sync)."""
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_flows_flow_alias_executions.sync_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body=execution_data
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update executions: {response.status_code}")

    async def aupdate_executions(self, realm: str | None = None, flow_alias: str = None, execution_data: AuthenticationExecutionInfoRepresentation = None) -> None:
        """Update executions for a flow (async)."""
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_flows_flow_alias_executions.asyncio_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body=execution_data
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update executions: {response.status_code}")

    # Authenticator Config
    def get_config(self, realm: str | None = None, config_id: str = None) -> AuthenticatorConfigRepresentation | None:
        """Get authenticator configuration (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_config_id.sync,
            realm=realm,
            id=config_id
        )

    async def aget_config(self, realm: str | None = None, config_id: str = None) -> AuthenticatorConfigRepresentation | None:
        """Get authenticator configuration (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_config_id.asyncio,
            realm=realm,
            id=config_id
        )

    def create_config(self, realm: str | None = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> str:
        """Create authenticator configuration (sync). Returns config ID."""
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_config.sync_detailed,
            realm=realm,
            body=config_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create config: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate_config(self, realm: str | None = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> str:
        """Create authenticator configuration (async). Returns config ID."""
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_config.asyncio_detailed,
            realm=realm,
            body=config_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create config: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def update_config(self, realm: str | None = None, config_id: str = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> None:
        """Update authenticator configuration (sync)."""
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_config_id.sync_detailed,
            realm=realm,
            id=config_id,
            body=config_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update config: {response.status_code}")

    async def aupdate_config(self, realm: str | None = None, config_id: str = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> None:
        """Update authenticator configuration (async)."""
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_config_id.asyncio_detailed,
            realm=realm,
            id=config_id,
            body=config_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update config: {response.status_code}")

    def delete_config(self, realm: str | None = None, config_id: str = None) -> None:
        """Delete authenticator configuration (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_authentication_config_id.sync_detailed,
            realm=realm,
            id=config_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete config: {response.status_code}")

    async def adelete_config(self, realm: str | None = None, config_id: str = None) -> None:
        """Delete authenticator configuration (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_authentication_config_id.asyncio_detailed,
            realm=realm,
            id=config_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete config: {response.status_code}")

    # Providers
    def get_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get authenticator providers (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_authenticator_providers.sync,
            realm
        )

    async def aget_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get authenticator providers (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_authenticator_providers.asyncio,
            realm
        )

    def get_client_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get client authenticator providers (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_client_authenticator_providers.sync,
            realm
        )

    async def aget_client_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get client authenticator providers (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_client_authenticator_providers.asyncio,
            realm
        )

    def get_form_action_providers(self, realm: str | None = None) -> list | None:
        """Get form action providers (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_form_action_providers.sync,
            realm
        )

    async def aget_form_action_providers(self, realm: str | None = None) -> list | None:
        """Get form action providers (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_form_action_providers.asyncio,
            realm
        )

    def get_form_providers(self, realm: str | None = None) -> list | None:
        """Get form providers (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_form_providers.sync,
            realm
        )

    async def aget_form_providers(self, realm: str | None = None) -> list | None:
        """Get form providers (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_form_providers.asyncio,
            realm
        )

    # Required Actions
    def get_required_actions(self, realm: str | None = None) -> list[RequiredActionProviderRepresentation] | None:
        """Get required actions (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_required_actions.sync,
            realm
        )

    async def aget_required_actions(self, realm: str | None = None) -> list[RequiredActionProviderRepresentation] | None:
        """Get required actions (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_required_actions.asyncio,
            realm
        )

    def get_required_action(self, realm: str | None = None, alias: str = None) -> RequiredActionProviderRepresentation | None:
        """Get a required action by alias (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_required_actions_alias.sync,
            realm=realm,
            alias=alias
        )

    async def aget_required_action(self, realm: str | None = None, alias: str = None) -> RequiredActionProviderRepresentation | None:
        """Get a required action by alias (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_required_actions_alias.asyncio,
            realm=realm,
            alias=alias
        )

    def update_required_action(self, realm: str | None = None, alias: str = None, action_data: dict | RequiredActionProviderRepresentation = None) -> None:
        """Update a required action (sync)."""
        action_obj = action_data if isinstance(action_data, RequiredActionProviderRepresentation) else RequiredActionProviderRepresentation.from_dict(action_data)
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_required_actions_alias.sync_detailed,
            realm=realm,
            alias=alias,
            body=action_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update required action: {response.status_code}")

    async def aupdate_required_action(self, realm: str | None = None, alias: str = None, action_data: dict | RequiredActionProviderRepresentation = None) -> None:
        """Update a required action (async)."""
        action_obj = action_data if isinstance(action_data, RequiredActionProviderRepresentation) else RequiredActionProviderRepresentation.from_dict(action_data)
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_required_actions_alias.asyncio_detailed,
            realm=realm,
            alias=alias,
            body=action_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update required action: {response.status_code}")

    def delete_required_action(self, realm: str | None = None, alias: str = None) -> None:
        """Delete a required action (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_authentication_required_actions_alias.sync_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete required action: {response.status_code}")

    async def adelete_required_action(self, realm: str | None = None, alias: str = None) -> None:
        """Delete a required action (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_authentication_required_actions_alias.asyncio_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete required action: {response.status_code}")

    def get_unregistered_required_actions(self, realm: str | None = None) -> list | None:
        """Get unregistered required actions (sync)."""
        return self._sync(
            get_admin_realms_realm_authentication_unregistered_required_actions.sync,
            realm
        )

    async def aget_unregistered_required_actions(self, realm: str | None = None) -> list | None:
        """Get unregistered required actions (async)."""
        return await self._async(
            get_admin_realms_realm_authentication_unregistered_required_actions.asyncio,
            realm
        )

    def register_required_action(self, realm: str | None = None, provider_data: dict = None) -> None:
        """Register a required action (sync)."""
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_register_required_action.sync_detailed,
            realm=realm,
            body=provider_data
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to register required action: {response.status_code}")

    async def aregister_required_action(self, realm: str | None = None, provider_data: dict = None) -> None:
        """Register a required action (async)."""
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_register_required_action.asyncio_detailed,
            realm=realm,
            body=provider_data
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to register required action: {response.status_code}")


class AuthenticationClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the AuthenticationAPI.
    """

    @cached_property
    def authentication(self) -> AuthenticationAPI:
        """Get the AuthenticationAPI instance."""
        return AuthenticationAPI(manager=self)  # type: ignore[arg-type]
