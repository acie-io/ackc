"""Keycloak management client CLI tool.

Maps the KeycloakManagementClient to a command-line interface for easy access to Keycloak management operations.
"""
import argparse
import json
import os
import sys

from ..management import KeycloakManagementClient


def handle_health(client: KeycloakManagementClient, args) -> None:
    """Handle health commands."""
    if args.health_type == "live":
        response = client.health_live()
    elif args.health_type == "ready":
        response = client.health_ready()
    elif args.health_type == "started":
        response = client.health_started()
    else:
        response = client.health()
    
    if args.json:
        print(json.dumps(response.to_dict(), indent=2))
    else:
        print(f"Status: {response.status}")
        if response.checks:
            for check in response.checks:
                print(f"  - {check.name}: {check.status}")


def handle_metrics(client: KeycloakManagementClient, args) -> None:
    """Handle metrics command."""
    if args.json:
        metrics = client.metrics_parsed()
        print(json.dumps(metrics, indent=2))
    else:
        print(client.metrics())


def main():
    parser = argparse.ArgumentParser(
        description="Keycloak Management Client - Access health and metrics endpoints",
        prog="auth-mc"
    )
    
    parser.add_argument(
        "--url",
        help="Management interface URL (defaults to KEYCLOAK_MANAGEMENT_URL env var)",
        default=os.environ.get("KEYCLOAK_MANAGEMENT_URL")
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    
    # Health command with subcommands
    health_parser = subparsers.add_parser("health", help="Check health status")
    health_subparsers = health_parser.add_subparsers(dest="health_type", help="Health check type")
    
    # Health subcommands
    health_subparsers.add_parser("live", help="Check liveness probe")
    health_subparsers.add_parser("ready", help="Check readiness probe")
    health_subparsers.add_parser("started", help="Check started probe")
    
    # Metrics command
    subparsers.add_parser("metrics", help="Get Prometheus metrics")
    
    args = parser.parse_args()
    
    try:
        client = KeycloakManagementClient(url=args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.command == "health":
            handle_health(client, args)
        elif args.command == "metrics":
            handle_metrics(client, args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
