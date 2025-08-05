import argparse
import json
import os
import sys
import base64
import asyncio
from getpass import getpass

from ..keycloak import KeycloakClient
from ..exceptions import AuthError


def main():
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
                        default=os.getenv('KEYCLOAK_URL', 'https://id.acie.dev'),
                        help='Keycloak server URL (default: KEYCLOAK_URL)')

    parser.add_argument('--realm',
                        default='acie',
                        help='Realm (default: acie)')

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

    args = parser.parse_args()
    
    if args.username and not args.password:
        parser.error("--username can only be used with --password")

    try:
        if args.device:
            client = KeycloakClient(
                server_url=args.server_url,
                client_id="dummy",
                client_secret="dummy",
            )
            token = asyncio.run(client.aget_token_device(
                realm=args.realm,
                client_id=args.client_id or 'dev-cli'
            ))
        elif args.password:
            username = args.username
            if not username:
                username = input("Username: " if not args.quiet else "")
            password = getpass(f"Password for {username}: " if not args.quiet else "")

            client = KeycloakClient(
                server_url=args.server_url,
                client_id=args.client_id or "admin-cli",
                client_secret=args.client_secret or "dummy",
            )
            token = client.get_token_password(
                username=username,
                password=password,
                realm=args.realm,
                client_id=args.client_id or 'admin-cli'
            )
        else:
            if not args.client_id or not args.client_secret:
                print("Error: Set KEYCLOAK_CLIENT_ID and KEYCLOAK_CLIENT_SECRET", file=sys.stderr)
                sys.exit(1)

            client = KeycloakClient(
                server_url=args.server_url,
                client_id=args.client_id,
                client_secret=args.client_secret,
            )
            token = client.get_token()

        if args.quiet:
            print(token.get('access_token', token))
        else:
            output = token.copy()

            if args.decode and 'access_token' in token:
                access_token = token['access_token']
                parts = access_token.split('.')
                if len(parts) == 3:
                    payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
                    decoded = base64.urlsafe_b64decode(payload)
                    output['claims'] = json.loads(decoded)

            print(json.dumps(output, indent=2))

    except AuthError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()
