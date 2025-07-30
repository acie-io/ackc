# ACKC - Acie API Client for Keycloak

A comprehensive Python client library for Keycloak Admin REST API, providing a clean and typed interface for managing Keycloak resources.

## Overview

ACKC (ACIE Keycloak Client) is a fully-typed Python library that wraps Keycloak's Admin REST API. It provides both synchronous and asynchronous interfaces for all major Keycloak administrative operations, with a focus on developer experience and type safety.

## Features

- **Complete API Coverage**: Implements all major Keycloak Admin API endpoints
- **Type Safety**: Full type annotations with attrs models for all requests and responses  
- **Async Support**: Both sync and async methods for all operations
- **Modern Python**: Built for Python 3.13+ using latest language features
- **Auto-generated Models**: Generated from Keycloak's OpenAPI specification for accuracy
- **Developer Friendly**: Clean API design with explicit parameters and comprehensive docstrings
- **Multiple Auth Methods**: Support for client credentials, password grant, and device code flows

## Installation

```bash
pip install ackc
```

For development with private package registry:
```bash
uv pip install ackc --index-url https://pypi.acie.dev/simple/
```

## Quick Start

```python
from ackc import KeycloakClient

# Initialize client with client credentials
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    client_id="admin-cli",
    client_secret="your-secret",
    realm="master"
)

with client:
    users = client.users.get_all()
    realms = client.realms.get_all()
```

## API Modules

ACKC organizes Keycloak's functionality into logical API modules:

### Users API (`client.users`)
Manage users, credentials, roles, and user sessions.
- Create, read, update, delete users
- Manage user credentials and password resets
- User role mappings and group memberships
- User sessions and consent management

[Keycloak Documentation: User Management](https://www.keycloak.org/docs/latest/server_admin/#user-management)

### Realms API (`client.realms`)
Configure realms, realm settings, and realm-level operations.
- Create and configure realms
- Manage realm settings and themes
- Default groups and client scopes
- Realm events and admin events
- Localization and internationalization

[Keycloak Documentation: Realms](https://www.keycloak.org/docs/latest/server_admin/#configuring-realms)

### Clients API (`client.clients`)
Manage OAuth2/OIDC clients and their configurations.
- Create and configure clients
- Client secrets and registration tokens
- Client scopes and protocol mappers
- Service accounts and permissions
- Client session management

[Keycloak Documentation: Clients](https://www.keycloak.org/docs/latest/server_admin/#oidc-clients)

### Roles API (`client.roles`)
Define and manage realm and client roles.
- Create realm and client roles
- Role hierarchies and composites
- Role permissions and attributes
- List role members

[Keycloak Documentation: Roles](https://www.keycloak.org/docs/latest/server_admin/#roles)

### Groups API (`client.groups`)
Organize users into groups with hierarchical structures.
- Create and manage groups
- Group hierarchies and subgroups
- Group role mappings
- Group members management

[Keycloak Documentation: Groups](https://www.keycloak.org/docs/latest/server_admin/#groups)

### Identity Providers API (`client.identity_providers`)
Configure external identity providers for federation.
- SAML and OIDC provider configuration
- Social login providers (Google, GitHub, etc.)
- Identity provider mappers
- First broker login flows

[Keycloak Documentation: Identity Providers](https://www.keycloak.org/docs/latest/server_admin/#identity-broker)

### Authentication API (`client.authentication`)
Customize authentication flows and requirements.
- Authentication flows and executions
- Required actions configuration
- Authenticator providers
- Password policies

[Keycloak Documentation: Authentication](https://www.keycloak.org/docs/latest/server_admin/#authentication-flows)

### Authorization API (`client.authorization`)
Fine-grained authorization using Keycloak Authorization Services.
- Resource servers and resources
- Authorization scopes and permissions
- Policies (role, group, time, JS, etc.)
- Policy evaluation and testing

[Keycloak Documentation: Authorization Services](https://www.keycloak.org/docs/latest/authorization_services/)

### Client Scopes API (`client.client_scopes`)
Manage reusable scope configurations for clients.
- Create and configure client scopes
- Protocol mappers for scopes
- Default and optional client scopes
- Scope evaluation

[Keycloak Documentation: Client Scopes](https://www.keycloak.org/docs/latest/server_admin/#client-scopes)

### Protocol Mappers API (`client.protocol_mappers`)
Configure how tokens and assertions are populated.
- Token claim mappings
- SAML attribute mappings
- User attribute and role mappings
- Hardcoded and dynamic values

[Keycloak Documentation: Protocol Mappers](https://www.keycloak.org/docs/latest/server_admin/#protocol-mappers)

### Components API (`client.components`)
Manage pluggable components like user storage providers.
- User storage providers (LDAP, custom)
- Key providers and keystores
- Theme providers
- Other SPI implementations

[Keycloak Documentation: User Storage](https://www.keycloak.org/docs/latest/server_admin/#user-storage-federation)

### Sessions API (`client.sessions`)
Monitor and manage active user and client sessions.
- List active sessions
- Session statistics
- Offline sessions
- Session revocation

[Keycloak Documentation: Sessions](https://www.keycloak.org/docs/latest/server_admin/#user-session-management)

### Events API (`client.events`)
Access and configure audit and admin events.
- Query login and admin events
- Configure event listeners
- Event types and details
- Event retention policies

[Keycloak Documentation: Events](https://www.keycloak.org/docs/latest/server_admin/#auditing-and-events)

### Keys API (`client.keys`)
Manage realm cryptographic keys.
- Active signing and encryption keys
- Key rotation
- Algorithm configuration
- Certificate management

[Keycloak Documentation: Keys](https://www.keycloak.org/docs/latest/server_admin/#realm-keys)

### Organizations API (`client.organizations`)
Manage organizations (Keycloak 25+).
- Organization management
- Organization members
- Organization identity providers
- Multi-tenancy support

[Keycloak Documentation: Organizations](https://www.keycloak.org/docs/latest/server_admin/#organizations)

## Authentication Methods

ACKC supports multiple authentication flows:

### Client Credentials (Recommended for M2M)
```python
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    client_id="admin-cli", 
    client_secret="secret"
)
```

### Password Grant (Legacy)
```python
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    username="admin",
    password="admin"
)
```

### Device Code Flow (CLI Tools)
```python
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    client_id="cli-client",
    use_device_code=True
)
```

### Existing Token
```python
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    token="existing-jwt-token"
)
```

## Async Support

All API methods have async equivalents:

```python
import asyncio
from ackc import KeycloakClient

async def main():
    client = KeycloakClient(
        server_url="https://keycloak.example.com",
        client_id="admin-cli",
        client_secret="secret"
    )

    async with client:
        # Use async methods to interact with Keycloak
        users = await client.users.aget_all()
        realms = await client.realms.aget_all()
        roles = await client.roles.aget_all()

asyncio.run(main())
```

## CLI Tools

ACKC includes helpful CLI tools:

### Get Token
```bash
auth-get-token --help
auth-get-token --server https://keycloak.example.com --client admin-cli
```

### Export Realm
```bash
auth-realm-export --help
auth-realm-export --server https://keycloak.example.com --realm my-realm
```

## Advanced Usage

### Custom Authentication
```python
# Use with CloudFlare Access (+ Tunnel = HTTPS for local development)

client = KeycloakClient(
    server_url="https://keycloak.example.com",
    cf_client_id='<your-cf-client-id>.access',  # or CF_ACCESS_CLIENT_ID
    cf_client_secret='your-cf-secret',  # or CF_ACCESS_CLIENT_SECRET
)
```

### Per-Request Realm Override
```python
# Initialize client for master realm
client = KeycloakClient(server_url="...", realm="master")

# Override realm for specific calls
users = client.users.get_all(realm="other-realm")
```

### Direct API Access

(Just don't do this)

## Error Handling

```python
from ackc import KeycloakClient, AuthError

try:
    with KeycloakClient(...) as client:
        users = client.users.get_all()

except AuthError as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## Development

### Regenerating API Client

To update the generated code when Keycloak API changes:

```bash
python scripts/generate_client.py
```

After generating, delete the generated `README.md` and `pyproject.toml` files, as they are not needed nor do they properly reflect the code.

## Requirements

- Python 3.13+
- Keycloak 26+ (tested with Keycloak 26.3)

## License

Private library - part of ACIE ecosystem.

## Contributing

This is currently a private library. For issues or contributions, please contact the ACIE team.

## See Also

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [Keycloak Admin REST API](https://www.keycloak.org/docs-api/latest/rest-api/)
