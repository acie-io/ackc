#!/usr/bin/env python
"""
Example of using the ACIE Keycloak client.

This shows how the generated code is directly accessible while still
having convenience wrappers for authentication.
"""
from ackc import KeycloakClient

# The client auto-authenticates using env vars
client = KeycloakClient()

# Option 1: Use convenience methods
print("Using convenience methods:")
users = client.get_users("master")
print(f"Found {len(users)} users")

# Option 2: Use the generated API directly
print("\nUsing generated API directly:")
from ackc.api.users import get_admin_realms_realm_users
response = get_admin_realms_realm_users.sync_detailed(
    realm="master",
    client=client.client,
    first=0,
    max_=10
)
print(f"Status: {response.status_code}")
print(f"Found {len(response.parsed)} users")

# Option 3: Access specific models
print("\nUsing generated models:")
from ackc.models import UserRepresentation
# Create a new user using the typed model
new_user = UserRepresentation(
    username="test_user",
    email="test@example.com",
    enabled=True,
    firstName="Test",
    lastName="User"
)

# All the generated API is discoverable via imports
# IDEs will show all available endpoints in acie.auth.client.api.*
# All models are in acie.auth.client.models.*