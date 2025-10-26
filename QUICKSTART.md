# PraisonAIWP Quick Start Guide

## Installation

### Using uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project
cd praisonaiwp
uv sync
```

### Using pip

```bash
cd praisonaiwp
pip install -e .
```

## Setup (One-Time)

```bash
praisonaiwp init
```

Follow the prompts to configure your WordPress server.

**💡 Tip:** If you have `~/.ssh/config` set up, just enter your host alias (e.g., `wp-prod`) and PraisonAIWP will automatically load username, key, and port from your SSH config!

## Usage Examples

### 1. Create a Single Post

```bash
praisonaiwp create "My First Post" --content "Hello World from PraisonAIWP!"
```

### 2. Create Multiple Posts from File

```bash
# Create example file
cat > posts.json << 'EOF'
[
  {
    "title": "Post 1",
    "content": "<p>Content for post 1</p>",
    "status": "publish"
  },
  {
    "title": "Post 2",
    "content": "<p>Content for post 2</p>",
    "status": "publish"
  }
]
EOF

# Create posts
praisonaiwp create posts.json
```

### 3. Update Specific Line in Post

```bash
# Replace text only at line 10
praisonaiwp update 123 "old heading" "new heading" --line 10
```

### 4. Update Nth Occurrence

```bash
# Replace only the 2nd occurrence
praisonaiwp update 123 "Welcome" "My Website" --nth 2
```

### 5. Preview Changes Before Applying

```bash
praisonaiwp update 123 "old" "new" --preview
```

### 6. Find Text in Posts

```bash
# Find in specific post
praisonaiwp find "example" 123

# Find across all posts
praisonaiwp find "example"

# Find in pages only
praisonaiwp find "example" --type page
```

### 7. List Posts

```bash
# List all posts
praisonaiwp list

# List pages
praisonaiwp list --type page

# List drafts
praisonaiwp list --status draft

# List with limit
praisonaiwp list --limit 10
```

## Real-World Example: Update 9 Language Pages

```bash
# Create updates file
cat > bulk_updates.json << 'EOF'
[
  {"post_id": 116, "line": 10, "find": "Old Heading", "replace": "New Title for Page 1"},
  {"post_id": 117, "line": 10, "find": "Old Heading", "replace": "New Title for Page 2"},
  {"post_id": 118, "line": 10, "find": "Old Heading", "replace": "New Title for Page 3"},
  {"post_id": 119, "line": 10, "find": "Old Heading", "replace": "New Title for Page 4"},
  {"post_id": 120, "line": 10, "find": "Old Heading", "replace": "New Title for Page 5"},
  {"post_id": 121, "line": 10, "find": "Old Heading", "replace": "New Title for Page 6"},
  {"post_id": 122, "line": 10, "find": "Old Heading", "replace": "New Title for Page 7"},
  {"post_id": 139, "line": 10, "find": "Old Heading", "replace": "New Title for Page 8"},
  {"post_id": 140, "line": 10, "find": "Old Heading", "replace": "New Title for Page 9"}
]
EOF

# Update all pages (one by one with preview for each)
for update in $(cat language_updates.json | jq -c '.[]'); do
  post_id=$(echo $update | jq -r '.post_id')
  line=$(echo $update | jq -r '.line')
  find=$(echo $update | jq -r '.find')
  replace=$(echo $update | jq -r '.replace')
  
  praisonaiwp update $post_id "$find" "$replace" --line $line
done
```

## Performance Tips

### Bulk Operations (100+ Posts)

When creating 100+ posts, PraisonAIWP automatically uses parallel mode:

```bash
# This will complete in ~8 seconds instead of 50+ seconds!
praisonaiwp create 100_posts.json
```

### Sequential vs Parallel

- **Sequential** (default for <10 posts): Simple, reliable, ~0.5s per post
- **Parallel** (auto for 10+ posts): 10x faster, ~5-8s for 100 posts

## Configuration

Edit `~/.praisonaiwp/config.yaml` to:
- Add multiple servers
- Change parallel threshold
- Adjust worker count
- Set default server

```yaml
settings:
  parallel_threshold: 10  # Use parallel mode for 10+ posts
  parallel_workers: 10    # Number of concurrent workers
  auto_backup: true       # Backup before updates
```

## Troubleshooting

### SSH Connection Failed

```bash
# Test SSH manually
ssh -i ~/.ssh/id_ed25519 user@hostname

# Check key permissions
chmod 600 ~/.ssh/id_ed25519
```

### WP-CLI Not Found

```bash
# Check WP-CLI path
ssh user@hostname "which wp"

# Update config with correct path
# Edit ~/.praisonaiwp/config.yaml
```

### PHP MySQL Extension Missing

```bash
# Use Plesk PHP binary
# Edit ~/.praisonaiwp/config.yaml
# Set php_bin: /opt/plesk/php/8.3/bin/php
```

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check [examples/](examples/) for more examples
- Run tests: `pytest`
- Contribute: Submit issues/PRs on GitHub

## Support

- GitHub Issues: https://github.com/yourusername/praisonaiwp/issues
- Documentation: https://praisonaiwp.readthedocs.io
