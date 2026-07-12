# Yuhi (यूँ ही)

> Python CLI toolkit to automate project enhancement using standard config templates.

## Overview

Yuhi is a command-line tool that helps you quickly set up and enhance Python projects by automating common configuration tasks like adding linting tools, licenses, GitHub workflows, and project structures.

## Features

- **Project Structure Creation**: Generate complete project structures from YAML templates
- **Code Quality Tools**: Automatically configure pre-commit, pylint, and sourcery
- **License Management**: Add licenses from GitHub templates
- **GitHub Integration**: Add standard GitHub files (SECURITY.md, CONTRIBUTING.md, etc.)
- **Package Scanning**: Scan dependencies for outdated or risky packages

## Installation

```bash
pipx install yuhi
```

## Quick Start

```bash
# View available commands
yuhi --help

# Add pre-commit configuration
yuhi add pre-commit

# Add pylint configuration
yuhi add pylint

# Create project structure from YAML
yuhi create files --structure-file project.yaml

# Scan dependencies for risky packages
yuhi scan
```

## Commands

| Command | Description |
|---------|-------------|
| `yuhi add` | Add facets (pre-commit, pylint, license, etc.) |
| `yuhi create` | Create complete project structure |
| `yuhi sample` | Generate sample configuration files |
| `yuhi scan` | Scan dependencies for outdated/risky packages |

## API Reference

Explore the [API Reference](api/cli.md) for detailed documentation of all modules.
