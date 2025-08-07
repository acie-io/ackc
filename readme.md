# ACKC - Acie API Client for Keycloak

A comprehensive Python client library for Keycloak Admin REST API, providing a clean and typed interface for managing Keycloak resources.

## Overview

ACKC is a fully-typed Python library that wraps Keycloak's Admin REST API.

It provides both synchronous and asynchronous interfaces for all major Keycloak administrative operations, with a focus on developer experience, type safety, and efficiency. The author of this package was also a little fed up with the usual daily slog of CLI login and token acquisition before getting to work, so this library aims to make that process as painless as possible.

## Features

- **Complete API Coverage**: 100% implementation of all 371 non-deprecated Keycloak Admin API endpoints
- **Type Safety**: Full type annotations with attrs models for all requests and responses  
- **Async Support**: Both sync and async methods for all operations
- **Modern Python**: Built for Python 3.13+ using latest language features
- **Auto-generated Models**: Generated from Keycloak's OpenAPI specification for accuracy
- **Developer Friendly**: Clean API design with explicit parameters and comprehensive docstrings
- **Multiple Auth Methods**: Support for client credentials, password grant, and device code flows

## Installation

`uv` is recommended, but you can also use other package managers like `pip`.

```bash
uv add ackc
```

## Quick Start

```python
from ackc import KeycloakClient

client = KeycloakClient(
    server_url="https://keycloak.example.com",
    client_id="admin-cli",
    client_secret="your-secret",
    realm="my-realm",  # Default realm for API calls
    auth_realm="master",  # Default realm for client authentication
)

with client:
    users = client.users.get_all()
    realms = client.realms.get_all()

async def main():
    async with client:
        await client.users.aget_all()
        await client.realms.aget_all()
```

## Authentication Methods

ACKC supports multiple authentication flows:

### Client Credentials (Default, Recommended for M2M)
```python
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    client_id="admin-cli", 
    client_secret="secret"
)
users = client.users.get_all()
```

### Password Grant (Legacy Flow)
```python
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    client_id="my-client",
    client_secret="secret"
)

token = client.get_token_password(
    username="admin",
    password="admin",
    scopes=["openid", "profile", "email"]
)
```

### Device Code Flow (For CLI Tools)
```python
client = KeycloakClient(
    server_url="https://keycloak.example.com",
    client_id="cli-client"
)

def device_callback(*, verification_uri, user_code, expires_in):
    print(f"Please visit: {verification_uri}")
    print(f"User code: {user_code}")
    print(f"You have {expires_in} seconds to authorize")

token = client.get_token_device(
    scopes=["openid", "offline_access"],
    callback=device_callback
)
```

### Working with JWTs

ACKC provides methods for validating and working with JWTs:

```python
claims = KeycloakClient.jwt_decode(jwt="your-jwt-token")
print(f"User: {claims.get('preferred_username')}")
print(f"Expires: {claims.get('exp')}")

needs_refresh = KeycloakClient.jwt_needs_refresh(jwt="your-jwt-token", buffer_seconds=300)

client = KeycloakClient(...)
user_info = client.jwt_userinfo(jwt="your-jwt-token")

token_info = client.jwt_introspect(jwt="your-jwt-token")

if token_info.get("active"):
    print(f"Token is valid for user: {token_info.get('username')}")

new_token = client.jwt_refresh(refresh_token="your-refresh-token")
```

## Async Support

All API methods have async equivalents with the `a` prefix, allowing for non-blocking operations:

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
        users = await client.users.aget_all()
        realms = await client.realms.aget_all()
        roles = await client.roles.aget_all()

asyncio.run(main())
```

## CLI Tools

ACKC includes helpful CLI tools:

### Get Token
```bash
auth-token --help
auth-token --server https://keycloak.example.com --client admin-cli
```

### Export Realm
```bash
auth-realm-export --help
auth-realm-export --server https://keycloak.example.com --realm my-realm
```

### Management Commands
```bash
auth-mc --help
auth-mc --url http://localhost:9000 --json metrics  # Dump Keycloak prometheus metrics
```
## Advanced Usage

### Cloudflare Access Integration
```python
# Use with Cloudflare Access (+ Tunnel = HTTPS for local development or secure remote management)
# Note: This gets you past Cloudflare, but you still need to authenticate with Keycloak.

client = KeycloakClient(
    server_url="https://keycloak.example.com",
    cf_client_id='<your-cf-client-id>.access',  # or CF_ACCESS_CLIENT_ID
    cf_client_secret='your-cf-secret',  # or CF_ACCESS_CLIENT_SECRET
)
```

### Per-Request Realm and Auth Realm Override
```python
# Initialize client for master realm
client = KeycloakClient(server_url="...", realm="master")

# Override realm for specific calls
users = client.users.get_all(realm="other-realm")

# Use a different realm for authentication.
# Recommended for backend production clients to maintain least privilege.
company_realm = "acie"
client = KeycloakClient(server_url="...", auth_realm=company_realm, realm=company_realm)
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
python gen/generate_client.py --download
```

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


## API Modules

ACKC organizes Keycloak's functionality into logical API modules:

### Users API (`client.users`)
Manage users, credentials, roles, and user sessions.
- Create, read, update, delete users
- Manage user credentials and password resets
- User role mappings and group memberships
- User sessions and consent management

[Keycloak Documentation: User Management](https://www.keycloak.org/docs/latest/server_admin/#assembly-managing-users_server_administration_guide)

### Realms API (`client.realms`)
Configure realms, realm settings, and realm-level operations.
- Create and configure realms
- Manage realm settings and themes
- Default groups and client scopes
- Realm events and admin events
- Localization and internationalization

[Keycloak Documentation: Realms](https://www.keycloak.org/docs/latest/server_admin/#_configuring-realms)

### Clients API (`client.clients`)
Manage OAuth2/OIDC clients and their configurations.
- Create and configure clients
- Client secrets and registration tokens
- Client scopes and protocol mappers
- Service accounts and permissions
- Client session management

[Keycloak Documentation: Clients](https://www.keycloak.org/docs/latest/server_admin/#_oidc_clients)

### Roles API (`client.roles`)
Define and manage realm and client roles.
- Create realm and client roles
- Role hierarchies and composites
- Role permissions and attributes
- List role members

[Keycloak Documentation: Roles](https://www.keycloak.org/docs/latest/server_admin/#proc-creating-realm-roles_server_administration_guide)

### Groups API (`client.groups`)
Organize users into groups with hierarchical structures.
- Create and manage groups
- Group hierarchies and subgroups
- Group role mappings
- Group members management

[Keycloak Documentation: Groups](https://www.keycloak.org/docs/latest/server_admin/#proc-managing-groups_server_administration_guide)

### Identity Providers API (`client.identity_providers`)
Configure external identity providers for federation.
- SAML and OIDC provider configuration
- Social login providers (Google, GitHub, etc.)
- Identity provider mappers
- First broker login flows

[Keycloak Documentation: Identity Providers](https://www.keycloak.org/docs/latest/server_admin/#_identity_broker)

### Authentication API (`client.authentication`)
Customize authentication flows and requirements.
- Authentication flows and executions
- Required actions configuration
- Authenticator providers
- Password policies

[Keycloak Documentation: Authentication](https://www.keycloak.org/docs/latest/server_admin/#_authentication-flows)

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

[Keycloak Documentation: Client Scopes](https://www.keycloak.org/docs/latest/server_admin/#_client_scopes)

### Protocol Mappers API (`client.protocol_mappers`)
Configure how tokens and assertions are populated.
- Token claim mappings
- SAML attribute mappings
- User attribute and role mappings
- Hardcoded and dynamic values

[Keycloak Documentation: Protocol Mappers](https://www.keycloak.org/docs/latest/server_admin/#_protocol-mappers)

### Components API (`client.components`)
Manage pluggable components like user storage providers.
- User storage providers (LDAP, custom)
- Key providers and keystores
- Theme providers
- Other SPI implementations

[Keycloak Documentation: User Storage](https://www.keycloak.org/docs/latest/server_admin/#_user-storage-federation)

### Sessions API (`client.sessions`)
Monitor and manage active user and client sessions.
- List active sessions
- Session statistics
- Offline sessions
- Session revocation

[Keycloak Documentation: Sessions](https://www.keycloak.org/docs/latest/server_admin/#managing-user-sessions)

### Events API (`client.events`)
Access and configure audit and admin events.
- Query login and admin events
- Configure event listeners
- Event types and details
- Event retention policies

[Keycloak Documentation: Events](https://www.keycloak.org/docs/latest/server_admin/#configuring-auditing-to-track-events)

### Keys API (`client.keys`)
Manage realm cryptographic keys.
- Active signing and encryption keys
- Key rotation
- Algorithm configuration
- Certificate management

[Keycloak Documentation: Keys](https://www.keycloak.org/docs/latest/server_admin/#realm_keys)

### Organizations API (`client.organizations`)
Manage organizations (Keycloak 25+).
- Organization management
- Organization members
- Organization identity providers
- Multi-tenancy support

[Keycloak Documentation: Organizations](https://www.keycloak.org/docs/latest/server_admin/#_managing_organizations)

### Scope Mappings API (`client.scope_mappings`)
Manage client and realm scope mappings for users and groups.
- Realm-level role mappings
- Client-level role mappings
- Available and effective roles
- Composite role resolution

[Keycloak Documentation: Role Mappings](https://www.keycloak.org/docs/latest/server_admin/#_role_mappings)

### Client Role Mappings API (`client.client_role_mappings`)
Manage client-specific role assignments.
- Assign client roles to users
- Assign client roles to groups
- List available client roles
- Composite client role management

[Keycloak Documentation: Client Roles](https://www.keycloak.org/docs/latest/server_admin/#client-roles)

### Role Mapper API (`client.role_mapper`)
Manage realm-level role assignments.
- Assign realm roles to users
- Assign realm roles to groups
- List available realm roles
- Effective role calculation

[Keycloak Documentation: Realm Roles](https://www.keycloak.org/docs/latest/server_admin/#realm-roles)

### Roles by ID API (`client.roles_by_id`)
Manage roles using their unique IDs.
- Role CRUD operations by ID
- Composite role management by ID
- Role permissions by ID
- Cross-realm role operations

[Keycloak Documentation: Role Management](https://www.keycloak.org/docs/latest/server_admin/#_roles)

### Attack Detection API (`client.attack_detection`)
Manage brute force attack detection.
- View brute force status for users
- Clear brute force flags for users
- Reset attack detection counters
- Manage lockout policies

[Keycloak Documentation: Attack Detection](https://www.keycloak.org/docs/latest/server_admin/#password-policies)

### Client Initial Access API (`client.client_initial_access`)
Manage initial access tokens for dynamic client registration.
- Create initial access tokens
- List active tokens
- Delete tokens
- Configure token policies

[Keycloak Documentation: Client Registration](https://www.keycloak.org/docs/latest/securing_apps/#_client_registration)

### Client Attribute Certificate API (`client.client_attribute_certificate`)
Manage client certificates and keystores.
- Generate new certificates
- Upload certificate chains
- Download keystores (JKS/PKCS12)
- Certificate information retrieval

[Keycloak Documentation: Client Certificates](https://www.keycloak.org/docs/latest/server_admin/#_client-certificate-authentication)

### Client Registration Policy API (`client.client_registration_policy`)
Manage policies for dynamic client registration.
- List available policy providers
- Configure registration policies
- Set default client configurations
- Validation rules for client registration

[Keycloak Documentation: Client Registration Policies](https://www.keycloak.org/docs/latest/securing_apps/#_client_registration_policies)

# Implementation Status

* **Total API Endpoints**: 371 generated endpoints (excluding 23 deprecated template endpoints)
* **Categories with Wrappers**: 21 of 21 (100%)  
* **Endpoints Implemented**: 371 of 371 (100% coverage of non-deprecated APIs)
* **Response Unwrapping**: Automatic unwrapping of wrapper types for cleaner API

| API Module                       | Endpoints | Coverage | Status                                                                                     |
|----------------------------------|-----------|----------|--------------------------------------------------------------------------------------------|
| **Users**                        | 33        | 100%     | Full CRUD, groups, sessions, credentials, consents, federated identity, profile management |
| **Realms**                       | 44        | 100%     | Full CRUD, events, admin events, default groups, client scopes, partial import/export      |
| **Clients**                      | 34        | 100%     | Full CRUD, sessions, scopes, revocation, registration tokens                               |
| **Roles**                        | 27        | 100%     | Full CRUD, composites, client roles, users/groups with role                                |
| **Groups**                       | 11        | 100%     | Full CRUD, members, children, count                                                        |
| **Identity Providers**           | 17        | 100%     | Full CRUD, mappers, import/export, mapper types                                            |
| **Authentication**               | 39        | 100%     | Flows, executions, required actions, configurations                                        |
| **Authorization**                | 31        | 100%     | Resource server, resources, scopes, policies, permissions                                  |
| **Client Scopes**                | 5         | 100%     | Full CRUD operations (excluding 5 deprecated template endpoints)                           |
| **Protocol Mappers**             | 14        | 100%     | Full mapper operations (excluding 7 deprecated template endpoints)                         |
| **Components**                   | 6         | 100%     | Component management and sub-types                                                         |
| **Sessions**                     | 5         | 100%     | Session management for realms, clients, users                                              |
| **Events**                       | 6         | 100%     | User events, admin events, configuration                                                   |
| **Keys**                         | 1         | 100%     | Realm key management                                                                       |
| **Organizations**                | 19        | 100%     | Full organization management (Keycloak 25+)                                                |
| **Scope Mappings**               | 22        | 100%     | Realm and client scope mappings for users/groups (excluding 11 deprecated templates)       |
| **Client Role Mappings**         | 10        | 100%     | User and group client role assignments and available roles                                 |
| **Role Mapper**                  | 12        | 100%     | User and group realm role assignments and effective roles                                  |
| **Roles by ID**                  | 10        | 100%     | Role operations by ID, composite management, cross-realm operations                        |
| **Attack Detection**             | 3         | 100%     | Brute force detection status and flag management                                           |
| **Client Initial Access**        | 3         | 100%     | Initial access tokens for dynamic client registration                                      |
| **Client Attribute Certificate** | 6         | 100%     | Certificate generation, upload, keystore management                                        |
| **Client Registration Policy**   | 1         | 100%     | Registration policy provider configuration                                                 |
