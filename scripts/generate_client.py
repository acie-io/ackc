"""
Generate Keycloak client with niquests HTTP backend.

This script automates the generation of a high-performance Keycloak client
using openapi-python-client with custom templates that use niquests instead
of httpx for better performance and HTTP/2 support.
"""
import shutil
import subprocess
import sys
from pathlib import Path


def generate_client():
    """Generate the Keycloak client with niquests backend."""
    root_dir = Path(__file__).parent.parent
    templates_dir = root_dir / "scripts" / "templates"
    output_dir = root_dir / "ackc" / "generated"
    openapi_spec = root_dir / "keycloak-openapi.json"
    config_file = root_dir / "openapi-config.yaml"

    if not openapi_spec.exists():
        print("ERROR: keycloak-openapi.json not found.")
        print("Download it from: https://www.keycloak.org/docs-api/latest/rest-api/openapi.json")
        sys.exit(1)

    if output_dir.exists():
        print(f"Cleaning existing generated files at {output_dir}")
        shutil.rmtree(output_dir)

    output_dir.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating client from {openapi_spec}")
    cmd = [
        "openapi-python-client",
        "generate",
        "--path", str(openapi_spec),
        "--custom-template-path", str(templates_dir),
        "--output-path", str(output_dir),
        "--config", str(config_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR: Generation failed")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)

    generated_client = output_dir / "keycloak_admin_rest_api_client"
    if generated_client.exists():
        print(f"Moving generated client from {generated_client} to {output_dir}")
        for item in generated_client.iterdir():
            shutil.move(str(item), str(output_dir / item.name))
        generated_client.rmdir()

    print(f"✅ Client generated successfully at {output_dir}")

    init_file = output_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text(
            '"""Auto-generated Keycloak client using niquests."""\n'
            'from .client import Client, AuthenticatedClient\n'
            '\n__all__ = "Client", "AuthenticatedClient"\n'
        )

    print("✅ Post-processing complete")


if __name__ == "__main__":
    generate_client()
