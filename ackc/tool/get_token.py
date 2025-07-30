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
        epilog="Examples:\n"
               "  %(prog)s                    # Client credentials\n"
               "  %(prog)s -q                 # Just the token\n"
               "  %(prog)s --decode           # Show JWT claims\n"
               "  %(prog)s --device           # Device flow (browser)\n"
               "  %(prog)s --password         # Password auth"
    )

    parser.add_argument('--server-url',
                        default=os.getenv('KEYCLOAK_URL', 'https://id.acie.dev'),
                        help='Keycloak server URL (default: $KEYCLOAK_URL)')

    parser.add_argument('--realm',
                        default='acie',
                        help='Realm (default: acie)')

    parser.add_argument('--client-id',
                        default=os.getenv('KEYCLOAK_CLIENT_ID'),
                        help='Client ID (default: $KEYCLOAK_CLIENT_ID)')

    parser.add_argument('--client-secret',
                        default=os.getenv('KEYCLOAK_CLIENT_SECRET'),
                        help='Client secret (default: $KEYCLOAK_CLIENT_SECRET)')

    parser.add_argument('--device', action='store_true',
                        help='Use device authorization flow')

    parser.add_argument('--password', action='store_true',
                        help='Use password grant')

    parser.add_argument('--username',
                        help='Username for password grant')

    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='Output only the token value')

    parser.add_argument('--decode',
                        action='store_true',
                        help='Decode and display JWT claims')

    args = parser.parse_args()

    try:
        if args.device:
            # Device flow doesn't need client credentials
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
            # Password flow
            username = args.username
            if not username:
                username = input("Username: ")
            password = getpass(f"Password for {username}: ")

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
            # Client credentials flow
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
            print(token)
        else:
            output = {
                'access_token': token,
                'token_type': 'Bearer',
            }

            if args.decode:
                parts = token.split('.')
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
    # except Exception as e:
    #     print(f"Error: {e}", file=sys.stderr)
    #     sys.exit(1)


if __name__ == '__main__':
    main()
