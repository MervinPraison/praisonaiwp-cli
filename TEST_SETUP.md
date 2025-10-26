# Test Setup Guide

## Option 1: Use Config File (Recommended)

### 1. Initialize Configuration

```bash
cd /Users/praison/crawler/praisonaiwp
uv run praisonaiwp init
```

Follow the prompts to configure your server:
- Hostname: Your server hostname or IP
- Username: Your SSH username
- SSH Key: Path to your SSH private key (default: `~/.ssh/id_ed25519`)
- WordPress Path: Path to WordPress installation
- PHP Binary: PHP binary path (auto-detected, or specify for Plesk: `/opt/plesk/php/8.3/bin/php`)

### 2. Run Test

```bash
uv run python test_real_server.py
```

The test will automatically load configuration from `~/.praisonaiwp/config.yaml`.

---

## Option 2: Use Environment Variables

### 1. Create .env File

```bash
cp .env.example .env
```

### 2. Edit .env

```bash
# Option A: Use config file server name
PRAISONAIWP_SERVER=default

# Option B: Override with environment variables
WP_HOSTNAME=your-server.com
WP_SSH_USER=your_ssh_username
WP_SSH_KEY=~/.ssh/id_ed25519
WP_SSH_PORT=22
WP_PATH=/var/www/html/wordpress
WP_PHP_BIN=php
WP_CLI_BIN=/usr/local/bin/wp

# For Plesk servers, use:
# WP_PHP_BIN=/opt/plesk/php/8.3/bin/php
```

### 3. Run Test

```bash
# Load .env and run
source .env
uv run python test_real_server.py
```

---

## Option 3: Command Line Environment Variables

```bash
WP_HOSTNAME=your-server.com \
WP_SSH_USER=your_username \
WP_SSH_KEY=~/.ssh/id_ed25519 \
WP_PATH=/var/www/html/wordpress \
WP_PHP_BIN=php \
uv run python test_real_server.py
```

---

## Configuration Priority

The test script uses this priority order:

1. **Config File** (`~/.praisonaiwp/config.yaml`) - Highest priority
2. **Environment Variables** - Fallback if config not found
3. **Default Values** - Last resort

---

## Quick Test

### Using Config (Recommended)

```bash
# Setup once
uv run praisonaiwp init

# Test anytime
uv run python test_real_server.py
```

### Using Environment Variables

```bash
# Set environment variables
export WP_HOSTNAME=your-server.com
export WP_SSH_USER=your_username
export WP_PATH=/var/www/html/wordpress

# Run test
uv run python test_real_server.py
```

---

## Verify Configuration

Before running the test, verify your SSH connection:

```bash
ssh -i ~/.ssh/id_ed25519 your_username@your-server.com
```

If this works, the test should work too!

---

## Troubleshooting

### Config Not Found

```bash
# Initialize config
uv run praisonaiwp init
```

### SSH Key Permission Error

```bash
chmod 600 ~/.ssh/id_ed25519
```

### Environment Variables Not Working

```bash
# Check if variables are set
echo $WP_HOSTNAME
echo $WP_SSH_USER

# Set them if missing
export WP_HOSTNAME=82.165.193.19
export WP_SSH_USER=wordpress_user
```

---

## What the Test Does

1. ✅ Loads configuration (from config file or env vars)
2. ✅ Tests SSH connection
3. ✅ Tests WP-CLI access
4. ✅ Creates test post (draft)
5. ✅ Tests line-specific update (line 2 only)
6. ✅ Verifies precision editing worked
7. ✅ Optionally cleans up test post

---

## Expected Output

```
✓ Loaded config from ~/.praisonaiwp/config.yaml
Using server: default

Step 1: Testing SSH Connection
✓ Connected to 82.165.193.19
✓ Command execution working

Step 2: Testing WP-CLI Access
✓ WP-CLI is working

Step 3: Creating Test Post
✓ Test post created successfully!
Post ID: 123

Step 4: Testing Line-Specific Update
Found 2 occurrence(s) of 'Test Post from PraisonAIWP'
✓ Line-specific update test PASSED!

Step 5: Cleanup
Delete test post? (y/n):
```
