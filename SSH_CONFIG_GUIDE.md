# SSH Config Support Guide

PraisonAIWP now supports `~/.ssh/config` for simplified SSH connection management!

## Benefits

✅ **No need to specify connection details** - Just use host aliases  
✅ **Reuse existing SSH config** - Works with your current setup  
✅ **Cleaner configuration** - Less duplication  
✅ **Standard SSH workflow** - Familiar to all developers  

---

## Quick Start

### 1. Setup SSH Config

Edit `~/.ssh/config`:

```ssh-config
Host myserver
    HostName 203.0.113.10
    User wordpress_user
    IdentityFile ~/.ssh/id_ed25519
    Port 22

Host mywordpress
    HostName example.com
    User wordpress_user
    IdentityFile ~/.ssh/id_rsa
    Port 22
```

### 2. Use in PraisonAIWP Config

When running `praisonaiwp init`, just enter the host alias:

```bash
praisonaiwp init

# Prompts:
Server hostname: myserver  # Just the alias!
# Username, key, port automatically loaded from SSH config
```

### 3. Or Use Directly in Code

```python
from praisonaiwp.core.ssh_manager import SSHManager

# Just specify the host alias - everything else loaded from SSH config
with SSHManager('myserver') as ssh:
    stdout, stderr = ssh.execute('wp --info')
    print(stdout)
```

---

## Configuration Priority

PraisonAIWP uses this priority order:

1. **Explicit parameters** (if provided)
2. **SSH config** (`~/.ssh/config`)
3. **Defaults** (port 22, etc.)

### Example

```python
# SSH config has:
# Host myserver
#     HostName example.com
#     User admin
#     Port 2222

# This will use SSH config values:
SSHManager('myserver')
# → Connects to example.com:2222 as admin

# This will override SSH config:
SSHManager('myserver', username='root', port=22)
# → Connects to example.com:22 as root
```

---

## Complete Example

### SSH Config (`~/.ssh/config`)

```ssh-config
# Production WordPress Server
Host wp-prod
    HostName 82.165.193.19
    User wordpress_user
    IdentityFile ~/.ssh/id_ed25519
    Port 22

# Staging WordPress Server  
Host wp-staging
    HostName staging.example.com
    User staging_user
    IdentityFile ~/.ssh/id_ed25519
    Port 22

# Development WordPress Server
Host wp-dev
    HostName localhost
    User developer
    IdentityFile ~/.ssh/id_rsa
    Port 2222
```

### PraisonAIWP Config (`~/.praisonaiwp/config.yaml`)

```yaml
version: "1.0"
default_server: production

servers:
  production:
    hostname: wp-prod  # SSH config alias!
    wp_path: /var/www/vhosts/example.com/httpdocs
    php_bin: /opt/plesk/php/8.3/bin/php
    wp_cli: /usr/local/bin/wp
  
  staging:
    hostname: wp-staging  # SSH config alias!
    wp_path: /var/www/html/wordpress
    php_bin: php
    wp_cli: /usr/local/bin/wp
  
  development:
    hostname: wp-dev  # SSH config alias!
    wp_path: /home/developer/wordpress
    php_bin: php
    wp_cli: wp
```

### Usage

```bash
# Use production (uses wp-prod from SSH config)
praisonaiwp create "Test Post" --content "Hello"

# Use staging (uses wp-staging from SSH config)
praisonaiwp create "Test Post" --content "Hello" --server staging

# Use development (uses wp-dev from SSH config)
praisonaiwp create "Test Post" --content "Hello" --server development
```

---

## Environment Variables with SSH Config

You can still use environment variables, and they'll work with SSH config:

```bash
# Set host alias
export WP_HOSTNAME=wp-prod

# SSH config will provide username, key, port
export WP_PATH=/var/www/html
export WP_PHP_BIN=php

# Run
praisonaiwp create "Test" --content "Hello"
```

---

## Advanced SSH Config Features

### Jump Hosts (Bastion)

```ssh-config
Host bastion
    HostName bastion.example.com
    User admin
    IdentityFile ~/.ssh/id_rsa

Host wp-behind-bastion
    HostName 10.0.0.5
    User wordpress
    IdentityFile ~/.ssh/id_rsa
    ProxyJump bastion
```

PraisonAIWP will automatically use the ProxyJump!

```python
# Automatically connects through bastion
SSHManager('wp-behind-bastion')
```

### Multiple Identity Files

```ssh-config
Host wp-multi-key
    HostName example.com
    User admin
    IdentityFile ~/.ssh/id_rsa
    IdentityFile ~/.ssh/id_ed25519
    IdentityFile ~/.ssh/id_ecdsa
```

PraisonAIWP will try all keys in order.

### Connection Multiplexing

```ssh-config
Host wp-*
    ControlMaster auto
    ControlPath ~/.ssh/control-%r@%h:%p
    ControlPersist 10m
```

Speeds up multiple connections to the same server!

---

## Disable SSH Config

If you want to disable SSH config support:

```python
from praisonaiwp.core.ssh_manager import SSHManager

# Disable SSH config, use explicit parameters only
ssh = SSHManager(
    hostname='example.com',
    username='user',
    key_file='~/.ssh/id_rsa',
    use_ssh_config=False  # Disable SSH config
)
```

---

## Testing SSH Config

### Test SSH Connection

```bash
# Test your SSH config works
ssh wp-prod

# If this works, PraisonAIWP will work too!
```

### Test with PraisonAIWP

```bash
# Test connection
uv run python -c "
from praisonaiwp.core.ssh_manager import SSHManager

with SSHManager('wp-prod') as ssh:
    stdout, _ = ssh.execute('echo Hello from SSH config!')
    print(stdout)
"
```

---

## Troubleshooting

### SSH Config Not Found

```bash
# Check if SSH config exists
ls -la ~/.ssh/config

# Create if missing
touch ~/.ssh/config
chmod 600 ~/.ssh/config
```

### Host Not in SSH Config

```bash
# List all hosts in SSH config
grep "^Host " ~/.ssh/config

# Add your host if missing
```

### Permission Denied

```bash
# Fix SSH config permissions
chmod 600 ~/.ssh/config

# Fix SSH key permissions
chmod 600 ~/.ssh/id_ed25519
```

### SSH Config Not Loading

Check logs for SSH config loading:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from praisonaiwp.core.ssh_manager import SSHManager
ssh = SSHManager('wp-prod')
# Will show: "Using SSH config for host: wp-prod"
```

---

## Migration Guide

### Before (Without SSH Config)

```yaml
# ~/.praisonaiwp/config.yaml
servers:
  production:
    hostname: 82.165.193.19
    username: wordpress_user
    key_file: ~/.ssh/id_ed25519
    port: 22
    wp_path: /var/www/html
```

### After (With SSH Config)

**SSH Config** (`~/.ssh/config`):
```ssh-config
Host wp-prod
    HostName 82.165.193.19
    User wordpress_user
    IdentityFile ~/.ssh/id_ed25519
    Port 22
```

**PraisonAIWP Config** (`~/.praisonaiwp/config.yaml`):
```yaml
servers:
  production:
    hostname: wp-prod  # Just the alias!
    wp_path: /var/www/html
    # username, key_file, port from SSH config
```

**Benefits:**
- ✅ Less duplication
- ✅ Reuse SSH config across tools
- ✅ Easier to maintain
- ✅ Standard SSH workflow

---

## Best Practices

1. **Use descriptive host aliases**: `wp-prod`, `wp-staging`, not `server1`, `server2`
2. **Keep SSH config organized**: Group related hosts together
3. **Use comments**: Document what each host is for
4. **Set permissions**: `chmod 600 ~/.ssh/config`
5. **Test connections**: `ssh host-alias` before using in PraisonAIWP
6. **Use ControlMaster**: Speed up multiple connections
7. **Backup SSH config**: It's important configuration!

---

## Summary

✅ **SSH config support is automatic** - No configuration needed  
✅ **Works with existing SSH config** - Reuse what you have  
✅ **Fallback to explicit parameters** - Still works without SSH config  
✅ **Standard SSH features** - ProxyJump, multiplexing, etc.  

**Start using SSH config aliases in PraisonAIWP today!** 🚀
