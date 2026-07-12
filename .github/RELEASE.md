# Release Process

## Overview

Yuhi uses **git tags as the single source of truth** for versioning. The version is automatically derived from git tags
during the build process using `hatch-vcs`, and `__about__.py` reads it from package metadata at runtime.

## How It Works

```
Git Tag (v0.0.9) 
    ↓
CI Triggered (on push)
    ↓
hatch-vcs reads tag → sets package version
    ↓
__about__.py reads version from package metadata
    ↓
Package built + published to PyPI + GitHub Release
```

## Making a Release

### 1. Prepare Your Code

Ensure all changes are committed on your release branch (usually `main`):

```bash
git status
git log --oneline -5
```

### 2. Create and Push Tag

```bash
git tag -a v0.0.9 -m "Release 0.0.9"
git push origin main
git push origin v0.0.9
```

### 3. CI Takes Over

Once you push the tag, GitHub Actions automatically:

1. ✅ Builds the package (hatch-vcs reads the tag and sets the version)
2. ✅ Creates a GitHub Release with auto-generated notes
3. ✅ Publishes to PyPI

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., `0.0.9`)
- Tags must start with `v` (e.g., `v0.0.9`)

### Development Versions

When building without a git tag, hatch-vcs generates dev versions:

```
0.0.8.dev1+gabc1234
```

This indicates 1 commit after v0.0.8, with git hash `abc1234`.

## Important Notes

### Never Edit `__about__.py` Manually

The file `src/__about__.py` reads the version from package metadata at runtime. It does not store a hardcoded version
string. The version is determined by the installed package, which gets it from git tags during build.

### If You Need to Re-release

If a release failed or you need to fix it:

```bash
# Delete the tag locally and remotely
git tag -d v0.0.9
git push --delete origin v0.0.9

# Fix your code, then re-tag
git tag -a v0.0.9 -m "Release 0.0.9"
git push origin v0.0.9
```

⚠️ **Warning:** Only do this if the release hasn't been published to PyPI yet. Never delete/recreate tags for published
releases.

## Testing Locally

Before tagging a release, test the build:

```bash
python -m build && twine check dist/*
```

The version in the built package should match your latest git tag.

## Troubleshooting

### Version shows as "unknown" or error

If you get an error or wrong version, ensure the package is properly installed:

```bash
pip install -e .
```

### Build shows wrong version

Ensure you have a git tag:

```bash
git tag -l
```

If no tags exist, create one:

```bash
git tag -a v0.0.9 -m "Release 0.0.9"
```

### CI workflow didn't trigger

Check that:

1. Tag name starts with `v` (e.g., `v0.0.9`)
2. Tag was pushed to the repository
3. GitHub Actions isn't disabled in repository settings
