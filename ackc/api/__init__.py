"""
Keycloak API accessor classes.

These classes provide a clean interface over the generated API code.
"""
from .base import *
from .users import *
from .realms import *
from .clients import *
from .roles import *
from .groups import *
from .organizations import *
from .identity_providers import *
from .client_scopes import *
from .components import *
from .sessions import *
from .events import *
from .authentication import *
from .authorization import *
from .protocol_mappers import *
from .keys import *

__all__ = (
    "AuthError", "AuthenticatedClient", "Client", "BaseAPI", "BaseClientManager",
    "UsersAPI", "UsersClientMixin", "UserRepresentation",
    "RealmsAPI", "RealmsClientMixin", "RealmRepresentation",
    "ClientsAPI", "ClientsClientMixin", "ClientRepresentation",
    "RolesAPI", "RolesClientMixin", "RoleRepresentation",
    "GroupsAPI", "GroupsClientMixin", "GroupRepresentation",
    "OrganizationsAPI", "OrganizationsClientMixin", "OrganizationRepresentation",
    "IdentityProvidersAPI", "IdentityProvidersClientMixin", "IdentityProviderRepresentation",
    "ClientScopesAPI", "ClientScopesClientMixin", "ClientScopeRepresentation",
    "ComponentsAPI", "ComponentsClientMixin", "ComponentRepresentation",
    "SessionsAPI", "SessionsClientMixin", "UserSessionRepresentation",
    "EventsAPI", "EventsClientMixin", "RealmEventsConfigRepresentation", "EventRepresentation", "AdminEventRepresentation",
    "AuthenticationAPI", "AuthenticationClientMixin", "AuthenticationFlowRepresentation", "AuthenticationExecutionInfoRepresentation", "AuthenticatorConfigRepresentation", "RequiredActionProviderRepresentation",
    "AuthorizationAPI", "AuthorizationClientMixin", "ResourceServerRepresentation", "ResourceRepresentation", "ScopeRepresentation", "AbstractPolicyRepresentation", "PolicyProviderRepresentation", "PolicyEvaluationResponse", "EvaluationResultRepresentation",
    "ProtocolMappersAPI", "ProtocolMappersClientMixin", "ProtocolMapperRepresentation",
    "KeysAPI", "KeysClientMixin", "KeysMetadataRepresentation",
    "KeycloakClientMixin",
)


class KeycloakClientMixin(
    UsersClientMixin,
    RealmsClientMixin,
    ClientsClientMixin,
    RolesClientMixin,
    GroupsClientMixin,
    OrganizationsClientMixin,
    IdentityProvidersClientMixin,
    ClientScopesClientMixin,
    ComponentsClientMixin,
    SessionsClientMixin,
    EventsClientMixin,
    AuthenticationClientMixin,
    AuthorizationClientMixin,
    ProtocolMappersClientMixin,
    KeysClientMixin,
):
    """
    Mixin that provides all Keycloak API methods in a single class.

    This allows using the Keycloak client without needing to instantiate
    separate API classes.

    Classes using this should also inherit from BaseKeycloakClient or BaseClientManager.
    """
