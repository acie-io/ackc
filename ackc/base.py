import asyncio
import os
import sys
import webbrowser

from .api import BaseClientManager, AuthenticatedClient, Client, AuthError

__all__ = (
    "AuthError",
    "BaseKeycloakClient",
)


class BaseKeycloakClient(BaseClientManager):
    """Base class to manage the authenticated client.
    """
    _auth_realm: str
    _client_config: dict[str, ...]
    _server_url: str
    _client_id: str
    _client_secret: str
    _token: str | None = None

    def __init__(
        self,
        realm: str | None = None, *,
        server_url: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        auth_realm: str = "master",
        verify_ssl: bool = True,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        cf_client_id: str | None = None,
        cf_client_secret: str | None = None,
        **kwds,
    ):
        """
        Initialize the Keycloak client.

        Args:
            realm: API realm to use (defaults to master)
            server_url: Keycloak server URL (defaults to KEYCLOAK_URL env var)
            client_id: OAuth2 client ID (defaults to KEYCLOAK_CLIENT_ID env var)
            client_secret: OAuth2 client secret (defaults to KEYCLOAK_CLIENT_SECRET env var)
            auth_realm: Realm to authenticate against (default: master)
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
            headers: Custom headers to include in requests
            cf_client_id: Cloudflare Access client ID
            cf_client_secret: Cloudflare Access client secret
            **kwds: Additional arguments for the underlying client
        """
        super().__init__(realm=realm)

        self._server_url = server_url or os.getenv("KEYCLOAK_URL")
        self._client_id = client_id or os.getenv("KEYCLOAK_CLIENT_ID")
        self._client_secret = client_secret or os.getenv("KEYCLOAK_CLIENT_SECRET")
        self._auth_realm = auth_realm

        if not self._client_id or not self._client_secret:
            raise AuthError(
                "Client credentials required. "
                "Set KEYCLOAK_CLIENT_ID and KEYCLOAK_CLIENT_SECRET env vars."
            )

        cf_client_id = cf_client_id or os.getenv("CF_ACCESS_CLIENT_ID")
        cf_client_secret = cf_client_secret or os.getenv("CF_ACCESS_CLIENT_SECRET")

        if cf_client_id and cf_client_secret:
            headers = (headers or {}) | {
                "CF-Access-Client-Id": cf_client_id,
                "CF-Access-Client-Secret": cf_client_secret
            }

        self._client_config = {
            "base_url": self._server_url,
            "verify_ssl": verify_ssl,
            "timeout": timeout,
            "headers": headers or {},
            **kwds
        }

    @property
    def auth_realm(self) -> str:
        """Keycloak authentication realm."""
        return self._auth_realm

    @property
    def server_url(self) -> str:
        """Keycloak server URL."""
        return self._server_url

    @property
    def client_id(self) -> str:
        """OAuth2 client ID."""
        return self._client_id

    @property
    def token(self) -> str | None:
        """Access token (does NOT trigger authentication).

        Use `get_token()` or `aget_token()` to ensure token retrieval.
        """
        return self._token

    def _ensure_authenticated(self):
        """Ensure we have a valid token and client."""
        if self._token is None:
            self._token = self._get_token()

        if self._client is None:
            self._client = AuthenticatedClient(
                token=self._token,
                **self._client_config
            )

    async def _ensure_authenticated_async(self):
        """Ensure we have a valid token and client (async)."""
        if self._token is None:
            self._token = await self._get_token_async()

        if self._client is None:
            self._client = AuthenticatedClient(
                token=self._token,
                **self._client_config
            )

    def _get_token(self) -> str:
        """Get an access token synchronously."""
        with Client(**self._client_config) as temp_client:
            token_url = f"{self.server_url}/realms/{self.auth_realm}/protocol/openid-connect/token"
            response = temp_client.get_niquests_client().post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                }
            )

            if response.status_code != 200:
                raise AuthError(f"Authentication failed: {response.status_code} - {response.text}")

            return response.json()["access_token"]

    async def _get_token_async(self) -> str:
        """Get an access token asynchronously."""
        async with Client(**self._client_config) as temp_client:
            token_url = f"{self.server_url}/realms/{self.auth_realm}/protocol/openid-connect/token"
            response = await temp_client.get_async_niquests_client().post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                }
            )

            if response.status_code != 200:
                raise AuthError(f"Authentication failed: {response.status_code} - {response.text}")

            return response.json()["access_token"]

    def get_token(self) -> str:
        """Get the current access token, authenticating if necessary."""
        self._ensure_authenticated()
        return self._token

    async def aget_token(self) -> str:
        """Get the current access token asynchronously, authenticating if necessary."""
        await self._ensure_authenticated_async()
        return self._token

    def refresh_token(self):
        """Refresh the access token synchronously."""
        self._token = self._get_token()
        if self._client:
            self._client.token = self._token

    async def arefresh_token(self):
        """Refresh the access token asynchronously."""
        self._token = await self._get_token_async()
        if self._client:
            self._client.token = self._token

    def get_token_password(
        self,
        username: str,
        password: str,
        realm: str = "acie",
        client_id: str = "admin-cli",
    ) -> str:
        """Get token using password grant (legacy flow)."""
        token_url = f"{self.server_url}/realms/{realm}/protocol/openid-connect/token"

        with Client(**self._client_config) as temp_client:
            response = temp_client.get_niquests_client().post(
                token_url,
                data={
                    "grant_type": "password",
                    "client_id": client_id,
                    "username": username,
                    "password": password,
                    "client_secret": self._client_secret if client_id == self.client_id else None,
                }
            )

            if response.status_code != 200:
                raise AuthError(f"Password authentication failed: {response.status_code} - {response.text}")

            return response.json()["access_token"]

    async def aget_token_password(
        self,
        username: str,
        password: str,
        realm: str = "acie",
        client_id: str = "admin-cli",
    ) -> str:
        """Get token using password grant (legacy flow) asynchronously."""
        token_url = f"{self.server_url}/realms/{realm}/protocol/openid-connect/token"

        async with Client(multiplexed=False, **self._client_config) as temp_client:
            response = await temp_client.get_async_niquests_client().post(
                token_url,
                data={
                    "grant_type": "password",
                    "client_id": client_id,
                    "username": username,
                    "password": password,
                    "client_secret": self._client_secret if client_id == self.client_id else None,
                }
            )

            if response.status_code != 200:
                raise AuthError(f"Password authentication failed: {response.status_code} - {response.text}")

            return response.json()["access_token"]

    async def aget_token_device(self, realm: str = "acie", client_id: str = "dev-cli") -> str:
        """Get token using device authorization flow (OAuth 2.1)."""
        device_url = f"{self.server_url}/realms/{realm}/protocol/openid-connect/auth/device"
        token_url = f"{self.server_url}/realms/{realm}/protocol/openid-connect/token"

        async with Client(multiplexed=False, **self._client_config) as temp_client:
            # Start device flow
            response = await temp_client.get_async_niquests_client().post(
                device_url,
                data={"client_id": client_id}
            )

            if response.status_code != 200:
                raise AuthError(f"Failed to start device flow: {response.status_code} - {response.text}")

            device_data = response.json()
            verification_uri = device_data.get('verification_uri_complete', device_data['verification_uri'])
            user_code = device_data['user_code']
            device_code = device_data['device_code']
            expires_in = device_data['expires_in']
            interval = device_data.get('interval', 5)

            print(f"Opening browser to: {verification_uri}", file=sys.stderr)
            print(f"User code: {user_code}", file=sys.stderr)

            try:
                webbrowser.open(verification_uri)
            except Exception as e:
                print(f"Failed to open browser: {e}", file=sys.stderr)

            # Poll for token
            start_time = asyncio.get_event_loop().time()

            while asyncio.get_event_loop().time() - start_time < expires_in:
                await asyncio.sleep(interval)

                response = await temp_client.get_async_niquests_client().post(
                    token_url,
                    data={
                        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                        'client_id': client_id,
                        'device_code': device_code,
                    }
                )

                if response.status_code == 200:
                    return response.json()['access_token']
                elif response.status_code == 400:
                    error = response.json().get('error', 'unknown_error')
                    if error == 'authorization_pending':
                        continue
                    elif error == 'slow_down':
                        interval += 5
                        continue
                    else:
                        raise AuthError(f"Device flow error: {error}")
                else:
                    raise AuthError(f"Token request failed: {response.status_code}")

            raise AuthError("Device authorization expired")
