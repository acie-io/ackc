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
    get_admin_realms_realm_authentication_executions_execution_id_config_id,
    post_admin_realms_realm_authentication_executions,
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
    get_admin_realms_realm_authentication_required_actions_alias_config,
    put_admin_realms_realm_authentication_required_actions_alias_config,
    delete_admin_realms_realm_authentication_required_actions_alias_config,
    get_admin_realms_realm_authentication_required_actions_alias_config_description,
    # Config descriptions
    get_admin_realms_realm_authentication_config_description_provider_id,
    get_admin_realms_realm_authentication_per_client_config_description,
)
from ..generated.models import (
    AuthenticationFlowRepresentation,
    AuthenticationExecutionInfoRepresentation,
    AuthenticatorConfigRepresentation,
    RequiredActionProviderRepresentation,
)
from ..exceptions import APIError

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
        """Get authentication flows (sync).
        
        Authentication flows define the sequence of authenticators for login.
        
        Args:
            realm: The realm name
            
        Returns:
            List of authentication flows configured in the realm
        """
        return self._sync(get_admin_realms_realm_authentication_flows.sync, realm)

    async def aget_flows(self, realm: str | None = None) -> list[AuthenticationFlowRepresentation] | None:
        """Get authentication flows (async).
        
        Authentication flows define the sequence of authenticators for login.
        
        Args:
            realm: The realm name
            
        Returns:
            List of authentication flows configured in the realm
        """
        return await self._async(get_admin_realms_realm_authentication_flows.asyncio, realm)

    def create_flow(self, realm: str | None = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Create an authentication flow (sync).
        
        Args:
            realm: The realm name
            flow_data: Flow configuration including alias and provider
            
        Raises:
            APIError: If flow creation fails
        """
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_flows.sync_detailed,
            realm=realm,
            body=flow_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create flow: {response.status_code}")

    async def acreate_flow(self, realm: str | None = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Create an authentication flow (async).
        
        Args:
            realm: The realm name
            flow_data: Flow configuration including alias and provider
            
        Raises:
            APIError: If flow creation fails
        """
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_flows.asyncio_detailed,
            realm=realm,
            body=flow_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create flow: {response.status_code}")

    def get_flow(self, realm: str | None = None, flow_id: str = None) -> AuthenticationFlowRepresentation | None:
        """Get an authentication flow by ID (sync).
        
        Args:
            realm: The realm name
            flow_id: Flow ID
            
        Returns:
            Authentication flow representation with full details
        """
        return self._sync(
            get_admin_realms_realm_authentication_flows_id.sync,
            realm=realm,
            id=flow_id
        )

    async def aget_flow(self, realm: str | None = None, flow_id: str = None) -> AuthenticationFlowRepresentation | None:
        """Get an authentication flow by ID (async).
        
        Args:
            realm: The realm name
            flow_id: Flow ID
            
        Returns:
            Authentication flow representation with full details
        """
        return await self._async(
            get_admin_realms_realm_authentication_flows_id.asyncio,
            realm=realm,
            id=flow_id
        )

    def update_flow(self, realm: str | None = None, flow_id: str = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Update an authentication flow (sync).
        
        Args:
            realm: The realm name
            flow_id: Flow ID to update
            flow_data: Updated flow configuration
            
        Raises:
            APIError: If flow update fails
        """
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_flows_id.sync_detailed,
            realm=realm,
            id=flow_id,
            body=flow_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update flow: {response.status_code}")

    async def aupdate_flow(self, realm: str | None = None, flow_id: str = None, flow_data: dict | AuthenticationFlowRepresentation = None) -> None:
        """Update an authentication flow (async).
        
        Args:
            realm: The realm name
            flow_id: Flow ID to update
            flow_data: Updated flow configuration
            
        Raises:
            APIError: If flow update fails
        """
        flow_obj = flow_data if isinstance(flow_data, AuthenticationFlowRepresentation) else AuthenticationFlowRepresentation.from_dict(flow_data)
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_flows_id.asyncio_detailed,
            realm=realm,
            id=flow_id,
            body=flow_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update flow: {response.status_code}")

    def delete_flow(self, realm: str | None = None, flow_id: str = None) -> None:
        """Delete an authentication flow (sync).
        
        Args:
            realm: The realm name
            flow_id: Flow ID to delete
            
        Raises:
            APIError: If flow deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_authentication_flows_id.sync_detailed,
            realm=realm,
            id=flow_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete flow: {response.status_code}")

    async def adelete_flow(self, realm: str | None = None, flow_id: str = None) -> None:
        """Delete an authentication flow (async).
        
        Args:
            realm: The realm name
            flow_id: Flow ID to delete
            
        Raises:
            APIError: If flow deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_authentication_flows_id.asyncio_detailed,
            realm=realm,
            id=flow_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete flow: {response.status_code}")

    def copy_flow(self, realm: str | None = None, flow_alias: str = None, new_name: str = None) -> None:
        """Copy an authentication flow (sync).
        
        Args:
            realm: The realm name
            flow_alias: Alias of the flow to copy
            new_name: Name for the new flow copy
            
        Raises:
            APIError: If flow copy fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_copy.sync_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body={"newName": new_name}
        )
        if response.status_code != 201:
            raise APIError(f"Failed to copy flow: {response.status_code}")

    async def acopy_flow(self, realm: str | None = None, flow_alias: str = None, new_name: str = None) -> None:
        """Copy an authentication flow (async).
        
        Args:
            realm: The realm name
            flow_alias: Alias of the flow to copy
            new_name: Name for the new flow copy
            
        Raises:
            APIError: If flow copy fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_copy.asyncio_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body={"newName": new_name}
        )
        if response.status_code != 201:
            raise APIError(f"Failed to copy flow: {response.status_code}")

    # Flow Executions
    def get_executions(self, realm: str | None = None, flow_alias: str = None) -> list[AuthenticationExecutionInfoRepresentation] | None:
        """Get executions for a flow (sync).
        
        Args:
            realm: The realm name
            flow_alias: Flow alias
            
        Returns:
            List of authentication executions in the flow
        """
        return self._sync(
            get_admin_realms_realm_authentication_flows_flow_alias_executions.sync,
            realm=realm,
            flow_alias=flow_alias
        )

    async def aget_executions(self, realm: str | None = None, flow_alias: str = None) -> list[AuthenticationExecutionInfoRepresentation] | None:
        """Get executions for a flow (async).
        
        Args:
            realm: The realm name
            flow_alias: Flow alias
            
        Returns:
            List of authentication executions in the flow
        """
        return await self._async(
            get_admin_realms_realm_authentication_flows_flow_alias_executions.asyncio,
            realm=realm,
            flow_alias=flow_alias
        )

    def update_executions(self, realm: str | None = None, flow_alias: str = None, execution_data: AuthenticationExecutionInfoRepresentation = None) -> None:
        """Update executions for a flow (sync).
        
        Args:
            realm: The realm name
            flow_alias: Flow alias
            execution_data: Updated execution configuration
            
        Raises:
            APIError: If execution update fails
        """
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_flows_flow_alias_executions.sync_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body=execution_data
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update executions: {response.status_code}")

    async def aupdate_executions(self, realm: str | None = None, flow_alias: str = None, execution_data: AuthenticationExecutionInfoRepresentation = None) -> None:
        """Update executions for a flow (async).
        
        Args:
            realm: The realm name
            flow_alias: Flow alias
            execution_data: Updated execution configuration
            
        Raises:
            APIError: If execution update fails
        """
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_flows_flow_alias_executions.asyncio_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body=execution_data
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update executions: {response.status_code}")

    # Authenticator Config
    def get_config(self, realm: str | None = None, config_id: str = None) -> AuthenticatorConfigRepresentation | None:
        """Get authenticator configuration (sync).
        
        Args:
            realm: The realm name
            config_id: Configuration ID
            
        Returns:
            Authenticator configuration representation
        """
        return self._sync(
            get_admin_realms_realm_authentication_config_id.sync,
            realm=realm,
            id=config_id
        )

    async def aget_config(self, realm: str | None = None, config_id: str = None) -> AuthenticatorConfigRepresentation | None:
        """Get authenticator configuration (async).
        
        Args:
            realm: The realm name
            config_id: Configuration ID
            
        Returns:
            Authenticator configuration representation
        """
        return await self._async(
            get_admin_realms_realm_authentication_config_id.asyncio,
            realm=realm,
            id=config_id
        )

    def create_config(self, realm: str | None = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> str:
        """Create authenticator configuration (sync).
        
        Args:
            realm: The realm name
            config_data: Authenticator configuration data
            
        Returns:
            Created configuration ID
            
        Raises:
            APIError: If configuration creation fails
        """
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_config.sync_detailed,
            realm=realm,
            body=config_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create config: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate_config(self, realm: str | None = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> str:
        """Create authenticator configuration (async).
        
        Args:
            realm: The realm name
            config_data: Authenticator configuration data
            
        Returns:
            Created configuration ID
            
        Raises:
            APIError: If configuration creation fails
        """
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_config.asyncio_detailed,
            realm=realm,
            body=config_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create config: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def update_config(self, realm: str | None = None, config_id: str = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> None:
        """Update authenticator configuration (sync).
        
        Args:
            realm: The realm name
            config_id: Configuration ID to update
            config_data: Updated configuration data
            
        Raises:
            APIError: If configuration update fails
        """
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_config_id.sync_detailed,
            realm=realm,
            id=config_id,
            body=config_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update config: {response.status_code}")

    async def aupdate_config(self, realm: str | None = None, config_id: str = None, config_data: dict | AuthenticatorConfigRepresentation = None) -> None:
        """Update authenticator configuration (async).
        
        Args:
            realm: The realm name
            config_id: Configuration ID to update
            config_data: Updated configuration data
            
        Raises:
            APIError: If configuration update fails
        """
        config_obj = config_data if isinstance(config_data, AuthenticatorConfigRepresentation) else AuthenticatorConfigRepresentation.from_dict(config_data)
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_config_id.asyncio_detailed,
            realm=realm,
            id=config_id,
            body=config_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update config: {response.status_code}")

    def delete_config(self, realm: str | None = None, config_id: str = None) -> None:
        """Delete authenticator configuration (sync).
        
        Args:
            realm: The realm name
            config_id: Configuration ID to delete
            
        Raises:
            APIError: If configuration deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_authentication_config_id.sync_detailed,
            realm=realm,
            id=config_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete config: {response.status_code}")

    async def adelete_config(self, realm: str | None = None, config_id: str = None) -> None:
        """Delete authenticator configuration (async).
        
        Args:
            realm: The realm name
            config_id: Configuration ID to delete
            
        Raises:
            APIError: If configuration deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_authentication_config_id.asyncio_detailed,
            realm=realm,
            id=config_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete config: {response.status_code}")

    # Providers
    def get_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get authenticator providers (sync).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available authenticator providers
        """
        return self._sync(
            get_admin_realms_realm_authentication_authenticator_providers.sync,
            realm
        )

    async def aget_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get authenticator providers (async).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available authenticator providers
        """
        return await self._async(
            get_admin_realms_realm_authentication_authenticator_providers.asyncio,
            realm
        )

    def get_client_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get client authenticator providers (sync).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available client authenticator providers
        """
        return self._sync(
            get_admin_realms_realm_authentication_client_authenticator_providers.sync,
            realm
        )

    async def aget_client_authenticator_providers(self, realm: str | None = None) -> list | None:
        """Get client authenticator providers (async).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available client authenticator providers
        """
        return await self._async(
            get_admin_realms_realm_authentication_client_authenticator_providers.asyncio,
            realm
        )

    def get_form_action_providers(self, realm: str | None = None) -> list | None:
        """Get form action providers (sync).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available form action providers
        """
        return self._sync(
            get_admin_realms_realm_authentication_form_action_providers.sync,
            realm
        )

    async def aget_form_action_providers(self, realm: str | None = None) -> list | None:
        """Get form action providers (async).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available form action providers
        """
        return await self._async(
            get_admin_realms_realm_authentication_form_action_providers.asyncio,
            realm
        )

    def get_form_providers(self, realm: str | None = None) -> list | None:
        """Get form providers (sync).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available form providers
        """
        return self._sync(
            get_admin_realms_realm_authentication_form_providers.sync,
            realm
        )

    async def aget_form_providers(self, realm: str | None = None) -> list | None:
        """Get form providers (async).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available form providers
        """
        return await self._async(
            get_admin_realms_realm_authentication_form_providers.asyncio,
            realm
        )

    # Required Actions
    def get_required_actions(self, realm: str | None = None) -> list[RequiredActionProviderRepresentation] | None:
        """Get required actions (sync).
        
        Required actions are actions users must complete before accessing resources.
        
        Args:
            realm: The realm name
            
        Returns:
            List of required action providers
        """
        return self._sync(
            get_admin_realms_realm_authentication_required_actions.sync,
            realm
        )

    async def aget_required_actions(self, realm: str | None = None) -> list[RequiredActionProviderRepresentation] | None:
        """Get required actions (async).
        
        Required actions are actions users must complete before accessing resources.
        
        Args:
            realm: The realm name
            
        Returns:
            List of required action providers
        """
        return await self._async(
            get_admin_realms_realm_authentication_required_actions.asyncio,
            realm
        )

    def get_required_action(self, realm: str | None = None, alias: str = None) -> RequiredActionProviderRepresentation | None:
        """Get a required action by alias (sync).
        
        Args:
            realm: The realm name
            alias: Required action alias
            
        Returns:
            Required action provider representation
        """
        return self._sync(
            get_admin_realms_realm_authentication_required_actions_alias.sync,
            realm=realm,
            alias=alias
        )

    async def aget_required_action(self, realm: str | None = None, alias: str = None) -> RequiredActionProviderRepresentation | None:
        """Get a required action by alias (async).
        
        Args:
            realm: The realm name
            alias: Required action alias
            
        Returns:
            Required action provider representation
        """
        return await self._async(
            get_admin_realms_realm_authentication_required_actions_alias.asyncio,
            realm=realm,
            alias=alias
        )

    def update_required_action(self, realm: str | None = None, alias: str = None, action_data: dict | RequiredActionProviderRepresentation = None) -> None:
        """Update a required action (sync).
        
        Args:
            realm: The realm name
            alias: Required action alias
            action_data: Updated action configuration
            
        Raises:
            APIError: If update fails
        """
        action_obj = action_data if isinstance(action_data, RequiredActionProviderRepresentation) else RequiredActionProviderRepresentation.from_dict(action_data)
        response = self._sync_detailed(
            put_admin_realms_realm_authentication_required_actions_alias.sync_detailed,
            realm=realm,
            alias=alias,
            body=action_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update required action: {response.status_code}")

    async def aupdate_required_action(self, realm: str | None = None, alias: str = None, action_data: dict | RequiredActionProviderRepresentation = None) -> None:
        """Update a required action (async).
        
        Args:
            realm: The realm name
            alias: Required action alias
            action_data: Updated action configuration
            
        Raises:
            APIError: If update fails
        """
        action_obj = action_data if isinstance(action_data, RequiredActionProviderRepresentation) else RequiredActionProviderRepresentation.from_dict(action_data)
        response = await self._async_detailed(
            put_admin_realms_realm_authentication_required_actions_alias.asyncio_detailed,
            realm=realm,
            alias=alias,
            body=action_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update required action: {response.status_code}")

    def delete_required_action(self, realm: str | None = None, alias: str = None) -> None:
        """Delete a required action (sync).
        
        Args:
            realm: The realm name
            alias: Required action alias to delete
            
        Raises:
            APIError: If deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_authentication_required_actions_alias.sync_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete required action: {response.status_code}")

    async def adelete_required_action(self, realm: str | None = None, alias: str = None) -> None:
        """Delete a required action (async).
        
        Args:
            realm: The realm name
            alias: Required action alias to delete
            
        Raises:
            APIError: If deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_authentication_required_actions_alias.asyncio_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete required action: {response.status_code}")

    def get_unregistered_required_actions(self, realm: str | None = None) -> list | None:
        """Get unregistered required actions (sync).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available but unregistered required actions
        """
        return self._sync(
            get_admin_realms_realm_authentication_unregistered_required_actions.sync,
            realm
        )

    async def aget_unregistered_required_actions(self, realm: str | None = None) -> list | None:
        """Get unregistered required actions (async).
        
        Args:
            realm: The realm name
            
        Returns:
            List of available but unregistered required actions
        """
        return await self._async(
            get_admin_realms_realm_authentication_unregistered_required_actions.asyncio,
            realm
        )

    def register_required_action(self, realm: str | None = None, provider_data: dict = None) -> None:
        """Register a required action (sync).
        
        Args:
            realm: The realm name
            provider_data: Provider configuration to register
            
        Raises:
            APIError: If registration fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_register_required_action.sync_detailed,
            realm=realm,
            body=provider_data
        )
        if response.status_code != 201:
            raise APIError(f"Failed to register required action: {response.status_code}")

    async def aregister_required_action(self, realm: str | None = None, provider_data: dict = None) -> None:
        """Register a required action (async).
        
        Args:
            realm: The realm name
            provider_data: Provider configuration to register
            
        Raises:
            APIError: If registration fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_register_required_action.asyncio_detailed,
            realm=realm,
            body=provider_data
        )
        if response.status_code != 201:
            raise APIError(f"Failed to register required action: {response.status_code}")

    def lower_required_action_priority(self, realm: str | None = None, alias: str = None) -> None:
        """Lower required action priority (sync).
        
        Args:
            realm: The realm name
            alias: Required action alias
            
        Raises:
            APIError: If priority change fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_required_actions_alias_lower_priority.sync_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to lower required action priority: {response.status_code}")

    async def alower_required_action_priority(self, realm: str | None = None, alias: str = None) -> None:
        """Lower required action priority (async).
        
        Args:
            realm: The realm name
            alias: Required action alias
            
        Raises:
            APIError: If priority change fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_required_actions_alias_lower_priority.asyncio_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to lower required action priority: {response.status_code}")

    def raise_required_action_priority(self, realm: str | None = None, alias: str = None) -> None:
        """Raise required action priority (sync).
        
        Args:
            realm: The realm name
            alias: Required action alias
            
        Raises:
            APIError: If priority change fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_required_actions_alias_raise_priority.sync_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to raise required action priority: {response.status_code}")

    async def araise_required_action_priority(self, realm: str | None = None, alias: str = None) -> None:
        """Raise required action priority (async).
        
        Args:
            realm: The realm name
            alias: Required action alias
            
        Raises:
            APIError: If priority change fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_required_actions_alias_raise_priority.asyncio_detailed,
            realm=realm,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to raise required action priority: {response.status_code}")

    # Execution management
    def add_execution(self, realm: str | None = None, flow_alias: str = None, provider: str = None) -> None:
        """Add new authentication execution (sync).
        
        Args:
            realm: The realm name
            flow_alias: Flow alias to add execution to
            provider: Provider ID for the execution
            
        Raises:
            APIError: If adding execution fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_executions_execution.sync_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body={"provider": provider}
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add execution: {response.status_code}")

    async def aadd_execution(self, realm: str | None = None, flow_alias: str = None, provider: str = None) -> None:
        """Add new authentication execution (async).
        
        Args:
            realm: The realm name
            flow_alias: Flow alias to add execution to
            provider: Provider ID for the execution
            
        Raises:
            APIError: If adding execution fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_executions_execution.asyncio_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body={"provider": provider}
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add execution: {response.status_code}")

    def add_flow_execution(self, realm: str | None = None, flow_alias: str = None, flow_data: dict = None) -> None:
        """Add new flow to execution (sync).
        
        Args:
            realm: The realm name
            flow_alias: Parent flow alias
            flow_data: Sub-flow configuration
            
        Raises:
            APIError: If adding flow execution fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_executions_flow.sync_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body=flow_data
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add flow execution: {response.status_code}")

    async def aadd_flow_execution(self, realm: str | None = None, flow_alias: str = None, flow_data: dict = None) -> None:
        """Add new flow to execution (async).
        
        Args:
            realm: The realm name
            flow_alias: Parent flow alias
            flow_data: Sub-flow configuration
            
        Raises:
            APIError: If adding flow execution fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_flows_flow_alias_executions_flow.asyncio_detailed,
            realm=realm,
            flow_alias=flow_alias,
            body=flow_data
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add flow execution: {response.status_code}")

    def get_execution(self, realm: str | None = None, execution_id: str = None) -> dict | None:
        """Get execution by ID (sync).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            
        Returns:
            Execution configuration
        """
        return self._sync(
            get_admin_realms_realm_authentication_executions_execution_id.sync,
            realm=realm,
            execution_id=execution_id
        )

    async def aget_execution(self, realm: str | None = None, execution_id: str = None) -> dict | None:
        """Get execution by ID (async).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            
        Returns:
            Execution configuration
        """
        return await self._async(
            get_admin_realms_realm_authentication_executions_execution_id.asyncio,
            realm=realm,
            execution_id=execution_id
        )

    def delete_execution(self, realm: str | None = None, execution_id: str = None) -> None:
        """Delete execution (sync).
        
        Args:
            realm: The realm name
            execution_id: Execution ID to delete
            
        Raises:
            APIError: If deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_authentication_executions_execution_id.sync_detailed,
            realm=realm,
            execution_id=execution_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete execution: {response.status_code}")

    async def adelete_execution(self, realm: str | None = None, execution_id: str = None) -> None:
        """Delete execution (async).
        
        Args:
            realm: The realm name
            execution_id: Execution ID to delete
            
        Raises:
            APIError: If deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_authentication_executions_execution_id.asyncio_detailed,
            realm=realm,
            execution_id=execution_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete execution: {response.status_code}")

    def create_execution_config(self, realm: str | None = None, execution_id: str = None, config_data: dict = None) -> None:
        """Create execution configuration (sync).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            config_data: Configuration data for execution
            
        Raises:
            APIError: If configuration creation fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_executions_execution_id_config.sync_detailed,
            realm=realm,
            execution_id=execution_id,
            body=config_data
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create execution config: {response.status_code}")

    async def acreate_execution_config(self, realm: str | None = None, execution_id: str = None, config_data: dict = None) -> None:
        """Create execution configuration (async).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            config_data: Configuration data for execution
            
        Raises:
            APIError: If configuration creation fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_executions_execution_id_config.asyncio_detailed,
            realm=realm,
            execution_id=execution_id,
            body=config_data
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create execution config: {response.status_code}")

    def lower_execution_priority(self, realm: str | None = None, execution_id: str = None) -> None:
        """Lower execution priority (sync).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            
        Raises:
            APIError: If priority change fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_executions_execution_id_lower_priority.sync_detailed,
            realm=realm,
            execution_id=execution_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to lower execution priority: {response.status_code}")

    async def alower_execution_priority(self, realm: str | None = None, execution_id: str = None) -> None:
        """Lower execution priority (async).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            
        Raises:
            APIError: If priority change fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_executions_execution_id_lower_priority.asyncio_detailed,
            realm=realm,
            execution_id=execution_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to lower execution priority: {response.status_code}")

    def raise_execution_priority(self, realm: str | None = None, execution_id: str = None) -> None:
        """Raise execution priority (sync).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            
        Raises:
            APIError: If priority change fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_authentication_executions_execution_id_raise_priority.sync_detailed,
            realm=realm,
            execution_id=execution_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to raise execution priority: {response.status_code}")

    async def araise_execution_priority(self, realm: str | None = None, execution_id: str = None) -> None:
        """Raise execution priority (async).
        
        Args:
            realm: The realm name
            execution_id: Execution ID
            
        Raises:
            APIError: If priority change fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_authentication_executions_execution_id_raise_priority.asyncio_detailed,
            realm=realm,
            execution_id=execution_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to raise execution priority: {response.status_code}")


class AuthenticationClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the AuthenticationAPI."""

    @cached_property
    def authentication(self) -> AuthenticationAPI:
        """Get the AuthenticationAPI instance.
        
        Returns:
            AuthenticationAPI instance for managing authentication flows
        """
        return AuthenticationAPI(manager=self)  # type: ignore[arg-type]
