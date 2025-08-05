"""
Keycloak client that provides a clean interface over the generated code.

This handles authentication and provides proper sync/async support without
requiring separate client classes.
"""
from urllib.parse import urlencode, urljoin

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
        
        # Direct access to generated API still works (not recommended for most use cases):
        from ackc.generated.api.users import get_admin_realms_realm_users
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

    def _build_url(self, path: str, **params) -> str:
        """Build a complete URL with server, path, and optional query parameters.
        
        Args:
            path: The URL path (relative to server_url)
            **params: Optional query parameters as keyword arguments
            
        Returns:
            The complete URL with encoded query parameters
        """
        full_url = urljoin(self.server_url, path.lstrip('/'))

        filtered_params = {k: v for k, v in params.items() if v is not None}
        if filtered_params:
            return f"{full_url}?{urlencode(filtered_params)}"
        return full_url

    def get_login_url(self, realm: str | None = None, **params) -> str:
        """Get the login URL for a specific realm.

        Args:
            realm: The realm name (defaults to instance realm)
            **params: Additional query parameters (e.g., client_id, response_type, scope, state)

        Returns:
            The login URL for the specified realm
        """
        return self._build_url(f"realms/{realm or self.realm}/protocol/openid-connect/auth", **params)

    @property
    def login_url(self) -> str:
        """Get the login URL for the default realm.

        Returns:
            The login URL for the default realm
        """
        return self.get_login_url(self.realm)

    @property
    def auth_login_url(self) -> str:
        """Get the login URL for the authentication realm.

        Returns:
            The login URL for the authentication realm (typically 'master')
        """
        return self.get_login_url(self.auth_realm)

    def check_registration_enabled(self, realm: str | None = None) -> bool:
        """Check if registration is enabled for a specific realm.

        Args:
            realm: The realm name (defaults to instance realm)

        Returns:
            True if registration is enabled, False otherwise
        """
        realm_data = self.realms.get(realm or self.realm)
        return bool(realm_data and getattr(realm_data, 'registration_allowed', False))

    async def acheck_registration_enabled(self, realm: str | None = None) -> bool:
        """Check if registration is enabled for a specific realm (async).

        Args:
            realm: The realm name (defaults to instance realm)

        Returns:
            True if registration is enabled, False otherwise
        """
        realm_data = await self.realms.aget(realm or self.realm)
        return bool(realm_data and getattr(realm_data, 'registration_allowed', False))

    def get_registration_url(self, realm: str | None = None, *, redirect_uri: str | None = None) -> str:
        """Get the registration URL for a specific realm if registration is enabled.

        Does not guarantee that registration is enabled; use `check_registration_enabled` first.

        Args:
            realm: The realm name (defaults to instance realm)
            redirect_uri: Optional redirect URI after successful registration

        Returns:
            The registration URL for the specified realm
        """
        return self._build_url(f"realms/{realm or self.realm}/protocol/openid-connect/registrations", redirect_uri=redirect_uri)

    @property
    def registration_url(self) -> str | None:
        """Get the registration URL for the default realm if registration is enabled.

        Returns:
            The registration URL for the default realm, or None if registration is disabled
        """
        return self.get_registration_url(self.realm)

    def export_realm_config(self, realm: str | None = None, *, include_users: bool = False) -> dict:
        """Export complete realm configuration for backup or migration.

        Args:
            realm: Realm name to export (defaults to instance realm)
            include_users: Whether to include users in export (can be large)

        Returns:
            Dictionary containing full realm configuration
        """
        realm = realm or self.realm
        config = {}

        realm_data = self.realms.get(realm)
        if realm_data:
            config["realm"] = realm_data.to_dict()

        clients = self.clients.get_all(realm) or []
        config["clients"] = [c.to_dict() for c in clients]

        client_scopes = self.client_scopes.get_all(realm) or []
        config["clientScopes"] = [cs.to_dict() for cs in client_scopes]

        idps = self.identity_providers.get_all(realm) or []
        config["identityProviders"] = [idp.to_dict() for idp in idps]

        flows = self.authentication.get_flows(realm) or []
        config["authenticationFlows"] = [f.to_dict() for f in flows]

        actions = self.authentication.get_required_actions(realm) or []
        config["requiredActions"] = [a.to_dict() for a in actions]

        roles = self.roles.get_all(realm) or []
        config["roles"] = {"realm": [r.to_dict() for r in roles]}

        groups = self.groups.get_all(realm) or []
        config["groups"] = groups

        components = self.components.get_all(realm) or []
        config["components"] = [c.to_dict() for c in components]

        events_config = self.events.get_events_config(realm)
        if events_config:
            config["eventsConfig"] = events_config.to_dict()

        if include_users:
            users = self.users.get_all(realm) or []
            config["users"] = [u.to_dict() for u in users]

        return config

    async def aexport_realm_config(self, realm: str | None = None, *, include_users: bool = False) -> dict:
        """Export complete realm configuration for backup or migration (async).
        
        Args:
            realm: Realm name to export (defaults to instance realm)
            include_users: Whether to include users in export (can be large)
            
        Returns:
            Dictionary containing full realm configuration
        """
        realm = realm or self.realm
        config = {}

        realm_data = await self.realms.aget(realm)
        if realm_data:
            config["realm"] = realm_data.to_dict()

        clients = await self.clients.aget_all(realm) or []
        config["clients"] = [c.to_dict() for c in clients]

        client_scopes = await self.client_scopes.aget_all(realm) or []
        config["clientScopes"] = [cs.to_dict() for cs in client_scopes]

        idps = await self.identity_providers.aget_all(realm) or []
        config["identityProviders"] = [idp.to_dict() for idp in idps]

        flows = await self.authentication.aget_flows(realm) or []
        config["authenticationFlows"] = [f.to_dict() for f in flows]

        actions = await self.authentication.aget_required_actions(realm) or []
        config["requiredActions"] = [a.to_dict() for a in actions]

        roles = await self.roles.aget_all(realm) or []
        config["roles"] = {"realm": [r.to_dict() for r in roles]}

        groups = await self.groups.aget_all(realm) or []
        config["groups"] = groups

        components = await self.components.aget_all(realm) or []
        config["components"] = [c.to_dict() for c in components]

        events_config = await self.events.aget_events_config(realm)
        if events_config:
            config["eventsConfig"] = events_config.to_dict()

        if include_users:
            users = await self.users.aget_all(realm) or []
            config["users"] = [u.to_dict() for u in users]

        return config
