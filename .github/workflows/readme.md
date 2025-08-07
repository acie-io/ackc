# GitHub Actions Workflows for ACKC

This directory contains GitHub Actions workflows for automated publishing of the ACKC package to PyPI.

## Workflows

### Publish to PyPI (`publish.yml`)
- **Trigger**: On push to main branch
- **Purpose**: Automatically publish new versions to PyPI when version changes
- **Actions**:
  1. Check if version in pyproject.toml has changed since last publish
  2. If changed, build the package
  3. Create GPG-signed tag (vX.Y.Z)
  4. Create simplified tag for major.minor (vX.Y)
  5. Push tags to repository
  6. Create GitHub release with changelog
  7. Publish to PyPI
  8. Update latest-publish tag for future comparisons

## Required Secrets

The following secrets must be configured in the GitHub repository settings:

- `PAT_TOKEN`: Personal Access Token with read/write permissions on Content
- `GPG_PRIVATE_KEY`: The GPG private key for signing commits and tags
- `GPG_PASSPHRASE`: The passphrase for the GPG key
- `PYPI_TOKEN`: The API token for publishing to PyPI

## Required Environment Variables

The following environment variables should be set in the `Publish` environment:

- `GPG_PUBLIC_KEY`: The GPG public key (informational)
- `PYPI_TOKEN_NAME`: The name of the PyPI token (informational)
- `SIGNED_COMMIT_USER`: The name for git commits
- `SIGNED_COMMIT_EMAIL`: The email for git commits

## Version Numbering

The version number follows the pattern `X.Y.Z` where:
- X = Major version (breaking changes)
- Y = Minor version (new features)
- Z = Patch version (bug fixes)

The workflow only publishes when the version in pyproject.toml is manually changed.

## Environment Configuration

The publish environment requires:
- `SIGNED_COMMIT_USER`: Git username for commits
- `SIGNED_COMMIT_EMAIL`: Git user email for commits

## Usage

**Publishing to PyPI**: 
1. Update version in pyproject.toml
2. Commit and push to main branch
3. Workflow will automatically detect version change and publish

## Branch Strategy

- **main**: Production branch - triggers PyPI releases

## Troubleshooting

- If git operations fail, ensure the PAT_TOKEN has sufficient permissions
- If GPG signing fails, ensure the GPG key is properly imported and the secrets are correct
- If PyPI publishing fails, check that the PYPI_TOKEN has sufficient permissions
