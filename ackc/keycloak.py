"""
Keycloak client that provides a clean interface over the generated code.

This handles authentication and provides proper sync/async support without
requiring separate client classes.
"""
from .api import KeycloakClientMixin
from .base import BaseKeycloakClient

__all__ = "KeycloakClient",


class KeycloakClient(KeycloakClientMixin, BaseKeycloakClient):
    """A unified Keycloak client that handles both sync and async operations.

    This client:
    - Auto-authenticates using environment variables or provided credentials
    - Provides a single interface for both sync and async operations
    - Handles token refresh automatically
    - Exposes the full generated API while adding convenience
    
    Usage:
        # Sync usage
        client = KeycloakClient()
        users = client.users.get_all("master")
        
        # Async usage - same client!
        async with client:
            users = await client.users.aget_all("master")
        
        # Direct access to generated API still works
        from acie.auth.client.api.users import get_admin_realms_realm_users
        users = get_admin_realms_realm_users.sync(realm="master", client=client.client)
    """
    realm: str = "acie"

    def __init__(
            self,
            realm: str | None = None, *,
            server_url: str | None = None,
            client_id: str | None = None,
            client_secret: str | None = None,
            auth_realm: str = "master",
            verify_ssl: bool = True,
            timeout: float = 30.0,
            **kwds
    ):
        """
        Initialize the Keycloak client.
        
        Args:
            server_url: Keycloak server URL (defaults to KEYCLOAK_URL env var)
            client_id: OAuth2 client ID (defaults to KEYCLOAK_CLIENT_ID env var)
            client_secret: OAuth2 client secret (defaults to KEYCLOAK_CLIENT_SECRET env var)
            auth_realm: Realm to authenticate against (default: master)
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
            **kwds: Additional arguments for the underlying client
        """
        super().__init__(
            realm=realm,
            server_url=server_url,
            client_id=client_id,
            client_secret=client_secret,
            auth_realm=auth_realm,
            verify_ssl=verify_ssl,
            timeout=timeout,
            **kwds
        )

    def export_realm_config(self, realm: str, include_users: bool = False) -> dict:
        """Export complete realm configuration for backup or migration.
        
        Args:
            realm: Realm name to export
            include_users: Whether to include users in export (can be large)
            
        Returns:
            Dictionary containing full realm configuration
        """
        config = {}

        # Get realm settings
        realm_data = self.realms.get(realm)
        if realm_data:
            config["realm"] = realm_data.to_dict() if hasattr(realm_data, 'to_dict') else realm_data

        # Get all clients
        clients = self.clients.get_all(realm) or []
        config["clients"] = [c.to_dict() if hasattr(c, 'to_dict') else c for c in clients]

        # Get all client scopes
        client_scopes = self.client_scopes.get_all(realm) or []
        config["clientScopes"] = [cs.to_dict() if hasattr(cs, 'to_dict') else cs for cs in client_scopes]

        # Get identity providers
        idps = self.identity_providers.get_all(realm) or []
        config["identityProviders"] = [idp.to_dict() if hasattr(idp, 'to_dict') else idp for idp in idps]

        # Get authentication flows
        flows = self.authentication.get_flows(realm) or []
        config["authenticationFlows"] = [f.to_dict() if hasattr(f, 'to_dict') else f for f in flows]

        # Get required actions
        actions = self.authentication.get_required_actions(realm) or []
        config["requiredActions"] = [a.to_dict() if hasattr(a, 'to_dict') else a for a in actions]

        # Get roles
        roles = self.roles.get_all(realm) or []
        config["roles"] = {"realm": [r.to_dict() if hasattr(r, 'to_dict') else r for r in roles]}

        # Get groups
        groups = self.groups.get_all(realm) or []
        config["groups"] = groups

        # Get components
        components = self.components.get_all(realm) or []
        config["components"] = [c.to_dict() if hasattr(c, 'to_dict') else c for c in components]

        # Get events config
        events_config = self.events.get_config(realm)
        if events_config:
            config["eventsConfig"] = events_config.to_dict() if hasattr(events_config, 'to_dict') else events_config

        # Optionally include users
        if include_users:
            users = self.users.get_all(realm) or []
            config["users"] = [u.to_dict() if hasattr(u, 'to_dict') else u for u in users]

        return config

    async def aexport_realm_config(self, realm: str, include_users: bool = False) -> dict:
        """Export complete realm configuration for backup or migration (async).
        
        Args:
            realm: Realm name to export
            include_users: Whether to include users in export (can be large)
            
        Returns:
            Dictionary containing full realm configuration
        """
        config = {}

        realm_data = await self.realms.aget(realm)
        if realm_data:
            config["realm"] = realm_data.to_dict() if hasattr(realm_data, 'to_dict') else realm_data

        clients = await self.clients.aget_all(realm) or []
        config["clients"] = [c.to_dict() if hasattr(c, 'to_dict') else c for c in clients]

        client_scopes = await self.client_scopes.aget_all(realm) or []
        config["clientScopes"] = [cs.to_dict() if hasattr(cs, 'to_dict') else cs for cs in client_scopes]

        idps = await self.identity_providers.aget_all(realm) or []
        config["identityProviders"] = [idp.to_dict() if hasattr(idp, 'to_dict') else idp for idp in idps]

        flows = await self.authentication.aget_flows(realm) or []
        config["authenticationFlows"] = [f.to_dict() if hasattr(f, 'to_dict') else f for f in flows]

        actions = await self.authentication.aget_required_actions(realm) or []
        config["requiredActions"] = [a.to_dict() if hasattr(a, 'to_dict') else a for a in actions]

        roles = await self.roles.aget_all(realm) or []
        config["roles"] = {"realm": [r.to_dict() if hasattr(r, 'to_dict') else r for r in roles]}

        groups = await self.groups.aget_all(realm) or []
        config["groups"] = groups

        components = await self.components.aget_all(realm) or []
        config["components"] = [c.to_dict() if hasattr(c, 'to_dict') else c for c in components]

        events_config = await self.events.aget_events_config(realm)
        if events_config:
            config["eventsConfig"] = events_config.to_dict() if hasattr(events_config, 'to_dict') else events_config

        if include_users:
            users = await self.users.aget_all(realm) or []
            config["users"] = [u.to_dict() if hasattr(u, 'to_dict') else u for u in users]

        return config
