---
layout: default
title: Transport Layer
description: Connect to WordPress via SSH, Kubernetes, or local subprocess
---

# Transport Layer

PraisonAIWP uses a pluggable transport system to execute WP-CLI commands on your WordPress server. All commands work identically regardless of which transport you use.

## Transport Types

| Transport | Use Case | Config Key | How It Works |
|-----------|----------|------------|--------------|
| **SSH** | Remote VPS / VM | `transport: ssh` (default) | Paramiko SSH connection |
| **Kubernetes** | K8s-deployed pods | `transport: kubernetes` | `kubectl exec` |
| **Local** | Same server | `transport: local` | Python `subprocess` |

## How It Works

```
praisonaiwp list --server mysite
       │
       ▼
  get_transport(config, "mysite")
       │
       ├── transport: ssh        → SSHManager (paramiko)
       ├── transport: kubernetes → KubernetesManager (kubectl exec)
       └── transport: local      → LocalTransport (subprocess)
       │
       ▼
  WPClient ← same interface for all transports
       │
       ▼
  wp post list --format=json
```

Every command file calls `get_transport()` — the factory reads your config and returns the right transport. You never need to change commands when switching transport types.

---

## SSH Transport (Default)

For traditional servers where you connect via SSH.

### Configuration

```yaml
servers:
  production:
    # transport: ssh  ← default, can be omitted
    hostname: example.com
    username: ubuntu
    port: 22
    key_file: ~/.ssh/id_rsa
    wp_path: /var/www/html
    wp_cli: /usr/local/bin/wp
    php_bin: php
```

### SSH Config Support

PraisonAIWP reads `~/.ssh/config` automatically. You can use SSH aliases:

```yaml
servers:
  production:
    hostname: my-server-alias   # matches Host in ~/.ssh/config
    wp_path: /var/www/html
```

### Requirements

- SSH access to the server
- WP-CLI installed on the server (auto-installed if missing)
- SSH key or password authentication

### Usage

```bash
praisonaiwp list --server production
praisonaiwp plugin list --server production
praisonaiwp create "My Post" --content "<p>Hello</p>" --server production
```

---

## Kubernetes Transport

For WordPress running in Kubernetes pods.

### Configuration

```yaml
servers:
  my-k8s-site:
    transport: kubernetes
    namespace: default              # K8s namespace
    pod_selector: app=wordpress     # Label selector to find the pod
    wp_path: /var/www/html          # WordPress path inside the container
    container: php-fpm              # Container name (multi-container pods)
    wp_cli: /usr/local/bin/wp       # WP-CLI path inside the container
    php_bin: php
```

### How Pod Resolution Works

1. PraisonAIWP uses the `pod_selector` to find a running pod via `kubectl get pods -l <selector>`
2. If the pod is recycled (e.g., during a deployment), it auto-re-resolves on the next command
3. You can also specify `pod_name` directly instead of `pod_selector`

### Requirements

- `kubectl` installed and configured
- Kubeconfig with access to the target namespace
- WP-CLI available inside the container (auto-installed if missing)

### File Transfer

File uploads use `kubectl cp` instead of SFTP:

```bash
praisonaiwp media upload /local/image.jpg --server my-k8s-site
```

### Usage

```bash
praisonaiwp list --server my-k8s-site
praisonaiwp plugin list --server my-k8s-site
praisonaiwp cache flush --server my-k8s-site
praisonaiwp doctor --server my-k8s-site
```

---

## Local Transport

For running PraisonAIWP directly on the WordPress server itself — no SSH needed.

### Configuration

```yaml
servers:
  local-site:
    transport: local
    wp_path: /var/www/html
    wp_cli: /usr/local/bin/wp
    allow_root: true           # Optional, auto-detected if running as root
```

### Auto-Detection

You don't always need `transport: local`. PraisonAIWP auto-detects local mode when:

| Condition | Auto-detected? |
|-----------|---------------|
| `hostname` is missing or empty | ✓ Yes |
| `hostname` is `localhost` or `127.0.0.1` | ✓ Yes |
| `hostname` matches the machine's own hostname | ✓ Yes |
| `hostname` is a remote server | ✗ No (uses SSH) |

#### Minimal Local Config (Auto-Detected)

```yaml
servers:
  my-site:
    wp_path: /var/www/html
```

No `transport`, no `hostname` — PraisonAIWP detects it's local and uses subprocess.

### How It Works

- Commands execute via Python's `subprocess.run()` with `shell=True`
- Working directory is set to `wp_path`
- File uploads become local `shutil.copy2()` operations
- `allow_root` is auto-detected when running as root (`uid=0`)

### Requirements

- WP-CLI installed on the local machine
- Read/write access to the WordPress directory
- PHP available in `$PATH`

### Usage

```bash
praisonaiwp list --server local-site
praisonaiwp plugin list --server local-site
praisonaiwp create "My Post" --content "<p>Hello</p>" --server local-site
```

---

## Mixed Environment Example

You can mix all three transport types in a single config:

```yaml
default_server: production

servers:
  # Remote VPS via SSH
  production:
    hostname: example.com
    username: ubuntu
    key_file: ~/.ssh/id_rsa
    wp_path: /var/www/html

  # Kubernetes cluster
  staging:
    transport: kubernetes
    namespace: staging
    pod_selector: app=wordpress
    container: php-fpm
    wp_path: /var/www/html

  # Local development
  dev:
    transport: local
    wp_path: /home/user/wordpress
```

Then use the same commands for all:

```bash
praisonaiwp list --server production    # SSH
praisonaiwp list --server staging       # Kubernetes
praisonaiwp list --server dev           # Local
```

---

## Troubleshooting

### SSH: Authentication Failed

```bash
# Verify SSH key permissions
chmod 600 ~/.ssh/id_rsa

# Test SSH connection manually
ssh -i ~/.ssh/id_rsa user@example.com "wp --info"
```

### Kubernetes: Pod Not Found

```bash
# Check pod status
kubectl get pods -l app=wordpress -n default

# Verify kubectl access
kubectl exec <pod-name> -- echo "connected"
```

### Local: Permission Denied

```bash
# Check WP-CLI access
wp --path=/var/www/html --info

# If running as root, ensure allow_root is set
# In config: allow_root: true
# Or WP-CLI: wp --allow-root
```

### Doctor Command

The `doctor` command shows which transport each server uses:

```bash
praisonaiwp doctor --server mysite
```
