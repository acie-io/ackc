"""Keycloak token acquisition tool.

This module provides both a CLI tool and reusable functions for obtaining
Keycloak tokens via various OAuth2 flows (client credentials, password, device).

CLI Usage:
    python -m ackc.tool.get_token                    # Client credentials
    python -m ackc.tool.get_token --device           # Device flow
    python -m ackc.tool.get_token --password         # Password flow
    python -m ackc.tool.get_token -q                 # Just the token
    python -m ackc.tool.get_token --decode           # Show JWT claims

Library Usage:
    from ackc.tool.get_token import run
    
    # With dict args (e.g., from Django)
    token = run({'server_url': 'https://keycloak.example.com', 'device': True})
    
    # With custom client factory
    def my_factory(**kwargs):
        return KeycloakClient(
            server_url=kwargs.get('server_url') or settings.KEYCLOAK_URL,
            realm=kwargs.get('realm') or settings.KEYCLOAK_REALM,
            client_id=kwargs.get('client_id') or settings.KEYCLOAK_CLIENT_ID,
            client_secret=kwargs.get('client_secret') or settings.KEYCLOAK_CLIENT_SECRET,
        )
    
    token = run(args, client_factory=my_factory)

Django Management Command Example:
    from django.core.management.base import BaseCommand
    from django.conf import settings
    from ackc.tool.token import init_parser, run, format_output
    from ackc import KeycloakClient
    
    class Command(BaseCommand):
        help = 'Get Keycloak access token'
        
        def add_arguments(self, parser):
            init_parser(parser)
        
        def handle(self, *args, **options):
            def django_client_factory(**kwargs):
                return KeycloakClient(
                    server_url=kwargs.get('server_url') or settings.KEYCLOAK_URL,
                    realm=kwargs.get('realm') or settings.KEYCLOAK_REALM,
                    client_id=kwargs.get('client_id') or settings.KEYCLOAK_CLIENT_ID,
                    client_secret=kwargs.get('client_secret') or settings.KEYCLOAK_CLIENT_SECRET,
                )

            token = run(options, client_factory=django_client_factory)
            output = format_output(token, options['quiet'], options['decode'])
            self.stdout.write(output)

"""
import argparse
import json
import os
import sys
import base64
from getpass import getpass

from ..keycloak import KeycloakClient
from ..exceptions import AuthError


def init_parser(parser=None):
    """Create and return the argument parser for get_token.
    
    Args:
        parser: Optional existing ArgumentParser to add arguments to.
                If None, creates a new parser with description and epilog.
    
    Returns:
        ArgumentParser with all get_token arguments added.
    """
    if parser is None:
        parser = argparse.ArgumentParser(
            description="Get an access token from Keycloak",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""Examples:
  %(prog)s                    # Client credentials
  %(prog)s -q                 # Just the token
  %(prog)s --decode           # Show JWT claims
  %(prog)s --device           # Device flow (browser)
  %(prog)s --password         # Password auth"""
        )

    parser.add_argument('--server-url',
                        default=os.getenv('KEYCLOAK_URL'),
                        help='Keycloak server URL (default: KEYCLOAK_URL)')

    parser.add_argument('--realm',
                        default=None,
                        help='Realm name')

    parser.add_argument('--client-id',
                        default=os.getenv('KEYCLOAK_CLIENT_ID'),
                        help='Client ID (default: KEYCLOAK_CLIENT_ID)')

    parser.add_argument('--client-secret',
                        default=os.getenv('KEYCLOAK_CLIENT_SECRET'),
                        help='Client secret (default: KEYCLOAK_CLIENT_SECRET)')

    auth_methods = parser.add_mutually_exclusive_group()
    
    auth_methods.add_argument('--device', action='store_true',
                        help='Use device authorization flow')

    auth_methods.add_argument('--password', action='store_true',
                        help='Use password grant')

    parser.add_argument('--username',
                        help='Username for password grant')

    print_options = parser.add_mutually_exclusive_group()

    print_options.add_argument('-q', '--quiet',
                        action='store_true',
                        help='Output only the token value')

    print_options.add_argument('--decode',
                        action='store_true',
                        help='Decode and display JWT claims')
    
    return parser



def validate_args(args):
    """Validate command line arguments."""
    if args.username and not args.password:
        raise ValueError("--username can only be used with --password")


def decode_jwt(access_token):
    """Decode JWT token and return claims."""
    parts = access_token.split('.')
    if len(parts) == 3:
        payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    return None


def default_client_factory(server_url=None, realm=None, client_id=None, client_secret=None):
    """Default factory for creating KeycloakClient instances from env vars."""
    return KeycloakClient(
        server_url=server_url or os.getenv('KEYCLOAK_URL', 'https://id.acie.dev'),
        realm=realm or os.getenv('KEYCLOAK_REALM', 'acie'),
        client_id=client_id or os.getenv('KEYCLOAK_CLIENT_ID', 'admin-cli'),
        client_secret=client_secret or os.getenv('KEYCLOAK_CLIENT_SECRET', ''),
    )


def get_token_device(server_url=None, realm=None, client_id=None, client_factory=None, quiet=False):
    """Get token using device authorization flow."""
    def device_callback(info):
        if not quiet:
            print(f"Open browser to: {info['verification_uri']}", file=sys.stderr)
            print(f"User code: {info['user_code']}", file=sys.stderr)
        try:
            import webbrowser
            webbrowser.open(info['verification_uri'])
        except Exception:
            pass
    
    if client_factory is None:
        client_factory = default_client_factory
    
    client = client_factory(
        server_url=server_url,
        realm=realm,
        client_id="dummy",
        client_secret="dummy",
    )
    
    return client.get_token_device(client_id=client_id or 'dev-cli', callback=device_callback)


def get_token_password(server_url=None, realm=None, username=None, password=None, client_id=None, client_secret=None, client_factory=None):
    """Get token using password grant."""
    if not username or not password:
        raise ValueError("username and password required")
    
    if client_factory is None:
        client_factory = default_client_factory
    
    client = client_factory(
        server_url=server_url,
        realm=realm,
        client_id=client_id or "admin-cli",
        client_secret=client_secret or "dummy",
    )
    
    return client.get_token_password(
        username=username,
        password=password,
        client_id=client_id or 'admin-cli'
    )


def get_token_client_credentials(server_url=None, realm=None, client_id=None, client_secret=None, client_factory=None):
    """Get token using client credentials grant."""
    if client_factory is None:
        client_factory = default_client_factory
    
    client = client_factory(
        server_url=server_url,
        realm=realm,
        client_id=client_id,
        client_secret=client_secret,
    )
    return client.get_token()


def format_output(token, quiet=False, decode=False):
    """Format token output based on options."""
    if quiet:
        return token.get('access_token', token)
    
    output = token.copy()
    
    if decode and 'access_token' in token:
        claims = decode_jwt(token['access_token'])
        if claims:
            output['claims'] = claims
    
    return json.dumps(output, indent=2)


def get_credentials(args):
    """Get credentials for password auth, prompting if needed."""
    username = args.username
    if not username:
        username = input("Username: " if not args.quiet else "")
    password = getpass(f"Password for {username}: " if not args.quiet else "")
    return username, password


def run(args, client_factory=None):
    """Run the token acquisition based on parsed arguments.
    
    Args:
        args: Parsed command line arguments (Namespace or dict)
        client_factory: Optional factory function for creating KeycloakClient instances
        
    Returns:
        Token dict with access_token, refresh_token, etc.
    """
    if isinstance(args, dict):
        args = argparse.Namespace(**args)
    
    validate_args(args)
    if args.device:
        token = get_token_device(
            args.server_url,
            args.realm,
            args.client_id,
            client_factory=client_factory,
            quiet=args.quiet
        )
    elif args.password:
        username, password = get_credentials(args)
        token = get_token_password(
            args.server_url,
            args.realm,
            username,
            password,
            args.client_id,
            args.client_secret,
            client_factory=client_factory
        )
    else:
        if not args.client_id or not args.client_secret:
            print("Error: Set KEYCLOAK_CLIENT_ID and KEYCLOAK_CLIENT_SECRET", file=sys.stderr)
            sys.exit(1)

        token = get_token_client_credentials(
            args.server_url,
            args.realm,
            args.client_id,
            args.client_secret,
            client_factory=client_factory
        )
    
    return token


def main():
    """Main entry point for CLI usage."""
    parser = init_parser()
    args = parser.parse_args()

    try:
        token = run(args)
        output = format_output(token, args.quiet, args.decode)
        print(output)

    except AuthError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()