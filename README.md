# PraisonAIWP

AI-powered WordPress content management framework with precision editing capabilities.

## Features

### Core Features
- 🚀 **Simple CLI** - Intuitive commands with helpful prompts
- ⚡ **Fast** - Auto-parallel mode for bulk operations (10x faster)
- 🎯 **Precise** - Line-specific and occurrence-specific text replacements
- 🔒 **Safe** - Auto-backup, preview mode, dry-run capabilities
- 🌐 **Multi-Server** - Manage multiple WordPress installations
- 📝 **Smart** - Auto-detects file formats and optimal settings

### New in v1.0.2 🎉
- 🔑 **SSH Config Support** - Use `~/.ssh/config` host aliases for simplified connection management
- 🔧 **WP-CLI Auto-Installer** - One-command WP-CLI installation with automatic OS detection (Ubuntu, Debian, CentOS, RHEL, Fedora, Alpine, macOS)
- 🔍 **WordPress Auto-Detection** - Automatically find WordPress installations on your server with multiple search strategies
- ⚡ **UV Package Manager** - 10-100x faster dependency management with modern tooling
- 🛡️ **Enhanced Error Handling** - Helpful error messages with installation instructions and troubleshooting
- 📊 **Installation Verification** - Automatic checks for WP-CLI and WordPress validity on startup

## Installation

### Using uv (Recommended - 10x faster!)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/yourusername/praisonaiwp
cd praisonaiwp
uv sync

# Run commands
uv run praisonaiwp init
```

### Using pip

```bash
pip install praisonaiwp

# Or install from source
git clone https://github.com/yourusername/praisonaiwp
cd praisonaiwp
pip install -e .
```

## Quick Start

### 1. Initialize Configuration

```bash
praisonaiwp init
```

**💡 Pro Tips:**
- Use SSH config alias (e.g., `wp-prod`) - connection details loaded automatically!
- Press Enter for WordPress path - auto-detection will find it for you
- PHP binary is auto-detected, or specify for Plesk: `/opt/plesk/php/8.3/bin/php`

**🔑 SSH Config Support:**

PraisonAIWP automatically reads from `~/.ssh/config`. If you have multiple hosts configured:

```ssh-config
# ~/.ssh/config
Host wp-prod
    HostName production.example.com
    User prod_user
    IdentityFile ~/.ssh/id_prod

Host wp-staging
    HostName staging.example.com
    User staging_user
    IdentityFile ~/.ssh/id_staging

Host wp-dev
    HostName localhost
    User dev_user
    Port 2222
    IdentityFile ~/.ssh/id_dev
```

Just enter the host alias (e.g., `wp-prod`, `wp-staging`, or `wp-dev`) when prompted for hostname, and PraisonAIWP will automatically load all connection details from your SSH config!

**Choosing Between Multiple Configs:**
- Each host alias is independent
- Use `--server` flag to specify which server to use:
  ```bash
  praisonaiwp create "Post" --server production
  praisonaiwp create "Post" --server staging
  ```
- Configure multiple servers in `~/.praisonaiwp/config.yaml`:
  ```yaml
  servers:
    production:
      hostname: wp-prod  # SSH config alias
      wp_path: /var/www/html
    staging:
      hostname: wp-staging  # SSH config alias
      wp_path: /var/www/staging
  ```

This will prompt you for:
- **Server hostname** - Can be IP, hostname, or SSH config alias (e.g., `wp-prod`)
- **SSH username** - Auto-loaded from SSH config if using alias
- **SSH key path** - Auto-loaded from SSH config if using alias  
- **WordPress path** - Press Enter to auto-detect, or specify manually
- **PHP binary** - Auto-detected, or specify custom path

### 2. Auto-Install WP-CLI (Optional)

If WP-CLI is not installed on your server:

```bash
# Automatically detect OS and install WP-CLI
praisonaiwp install-wp-cli -y

# Install with dependencies (curl, php)
praisonaiwp install-wp-cli --install-deps -y

# Custom installation path
praisonaiwp install-wp-cli --install-path /usr/bin/wp

# For Plesk servers
praisonaiwp install-wp-cli --php-bin /opt/plesk/php/8.3/bin/php -y
```

**Supported Operating Systems:**
- ✅ Ubuntu (18.04, 20.04, 22.04, 24.04)
- ✅ Debian (9, 10, 11, 12)
- ✅ CentOS (7, 8, 9)
- ✅ RHEL (7, 8, 9)
- ✅ Fedora (35+)
- ✅ Alpine Linux
- ✅ macOS (with Homebrew)

**What it does:**
1. Detects your server's operating system
2. Downloads WP-CLI from official source
3. Tests the download
4. Makes it executable
5. Installs to system path
6. Verifies installation
7. Updates your config automatically

### 3. Auto-Detect WordPress (Optional)

If you don't know your WordPress installation path:

```bash
# Find all WordPress installations
praisonaiwp find-wordpress

# Interactive selection from multiple installations
praisonaiwp find-wordpress --interactive

# Find and update config automatically
praisonaiwp find-wordpress --update-config

# Find on different server
praisonaiwp find-wordpress --server staging
```

**Search Strategies:**
- Searches for `wp-config.php` in common directories
- Checks predefined paths (`/var/www/html`, `/var/www/vhosts/*/httpdocs`, etc.)
- Verifies each installation (wp-config, wp-content, wp-includes)
- Extracts WordPress version
- Interactive selection for multiple installations

**Example Output:**
```
✓ Found 2 WordPress installation(s)

┏━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ # ┃ Path                                ┃ Version ┃ Components              ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1 │ /var/www/html                       │ 6.4.2   │ config, content, includes│
│ 2 │ /var/www/vhosts/example.com/httpdocs│ 6.3.1   │ config, content, includes│
└───┴─────────────────────────────────────┴─────────┴─────────────────────────┘
```

### 4. Create Posts

```bash
# Single post
praisonaiwp create "My Post Title" --content "Post content here"

# From file (auto-detects JSON/YAML/CSV)
praisonaiwp create posts.json

# Create 100 posts (automatically uses parallel mode!)
praisonaiwp create 100_posts.json
```

### 5. Update Posts

```bash
# Update all occurrences
praisonaiwp update 123 "old text" "new text"

# Update specific line only
praisonaiwp update 123 "old text" "new text" --line 10

# Update 2nd occurrence only
praisonaiwp update 123 "old text" "new text" --nth 2

# Preview changes first
praisonaiwp update 123 "old text" "new text" --preview
```

### 6. Find Text

```bash
# Find in specific post
praisonaiwp find "search text" 123

# Find across all posts
praisonaiwp find "search text"

# Find in pages
praisonaiwp find "search text" --type page
```

### 7. List Posts

```bash
# List all posts
praisonaiwp list

# List pages
praisonaiwp list --type page

# List drafts
praisonaiwp list --status draft
```

## File Formats

### JSON Format

```json
[
  {
    "title": "Post Title",
    "content": "<p>Post content</p>",
    "status": "publish",
    "type": "post"
  }
]
```

### YAML Format

```yaml
- title: Post Title
  content: <p>Post content</p>
  status: publish
  type: post
```

### CSV Format

```csv
title,content,status,type
"Post Title","<p>Post content</p>",publish,post
```

## Configuration

Configuration is stored in `~/.praisonaiwp/config.yaml`:

```yaml
version: "1.0"
default_server: default

servers:
  default:
    hostname: example.com
    username: user
    key_file: ~/.ssh/id_ed25519
    port: 22
    wp_path: /var/www/html
    php_bin: /opt/plesk/php/8.3/bin/php
    wp_cli: /usr/local/bin/wp

settings:
  auto_backup: true
  parallel_threshold: 10
  parallel_workers: 10
  ssh_timeout: 30
  log_level: INFO
```

## Advanced Usage

### Line-Specific Replacement

When the same text appears multiple times but you only want to replace it at a specific line:

```bash
# Replace only at line 10
praisonaiwp update 123 "Welcome" "My Website" --line 10
```

### Occurrence-Specific Replacement

Replace only the 1st, 2nd, or nth occurrence:

```bash
# Replace only the 2nd occurrence
praisonaiwp update 123 "Welcome" "My Website" --nth 2
```

### Bulk Operations

Create 100 posts in ~8 seconds (vs 50+ seconds sequential):

```bash
# Automatically uses parallel mode for files with >10 posts
praisonaiwp create 100_posts.json
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

## Development

```bash
# Clone repository
git clone https://github.com/yourusername/praisonaiwp
cd praisonaiwp

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=praisonaiwp

# Format code
black praisonaiwp/

# Lint
flake8 praisonaiwp/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

Praison

## Links

- GitHub: https://github.com/yourusername/praisonaiwp
- Documentation: https://praisonaiwp.readthedocs.io
- PyPI: https://pypi.org/project/praisonaiwp
