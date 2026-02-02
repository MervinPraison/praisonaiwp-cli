# MCP Server Command

Connect PraisonAIWP to Claude Desktop, Cursor, VS Code, and other MCP (Model Context Protocol) clients.

!!! info "New in v1.3.0"
    MCP support enables AI assistants to manage WordPress directly through the Model Context Protocol.

## Installation

```bash
# Install with MCP support
pip install praisonaiwp[mcp]
```

## Quick Start

```bash
# View available tools
praisonaiwp mcp info

# Run MCP server
praisonaiwp mcp run

# Install in Claude Desktop
praisonaiwp mcp install
```

## Features

| Feature | Description |
|---------|-------------|
| **23 WordPress Tools** | Create, update, delete posts, manage users, plugins, themes |
| **8 Resources** | Read-only access to WordPress data |
| **4 Prompt Templates** | Blog post creation, SEO optimization, bulk updates |
| **Multiple Transports** | stdio (default) and HTTP |
| **Claude Desktop Integration** | One-command installation |
| **57 Tests** | 100% passing, production-ready |

## Available Tools

### Posts
| Tool | Description |
|------|-------------|
| `create_post` | Create a new post |
| `update_post` | Update existing post |
| `delete_post` | Delete a post |
| `get_post` | Get post details |
| `list_posts` | List all posts |
| `find_text` | Find text in posts |

### Categories
| Tool | Description |
|------|-------------|
| `list_categories` | List all categories |
| `set_post_categories` | Set post categories |
| `create_term` | Create new term |

### Users
| Tool | Description |
|------|-------------|
| `list_users` | List all users |
| `create_user` | Create new user |
| `get_user` | Get user details |

### Plugins
| Tool | Description |
|------|-------------|
| `list_plugins` | List installed plugins |
| `activate_plugin` | Activate a plugin |
| `deactivate_plugin` | Deactivate a plugin |

### Themes
| Tool | Description |
|------|-------------|
| `list_themes` | List installed themes |
| `activate_theme` | Activate a theme |

### Media
| Tool | Description |
|------|-------------|
| `import_media` | Import media files |

### System
| Tool | Description |
|------|-------------|
| `flush_cache` | Flush WordPress cache |
| `get_core_version` | Get WordPress version |
| `db_query` | Execute database query |
| `search_replace` | Search and replace in database |
| `wp_cli` | Run any WP-CLI command |

## Claude Desktop Integration

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "praisonaiwp": {
      "command": "praisonaiwp",
      "args": ["mcp", "run"]
    }
  }
}
```

Or use the automatic installer:

```bash
praisonaiwp mcp install
```

## Subcommands

### mcp info

Display available MCP tools, resources, and prompts.

```bash
praisonaiwp mcp info
```

### mcp run

Start the MCP server.

```bash
praisonaiwp mcp run [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--transport` | string | stdio | Transport type: stdio, http |
| `--port` | int | 8080 | HTTP port (when using http transport) |
| `--server` | string | - | Server name from config |

### mcp install

Install MCP server in Claude Desktop.

```bash
praisonaiwp mcp install
```

## Example Usage with Claude

Once configured, you can ask Claude to:

- "Create a new blog post about AI trends"
- "List all draft posts on my WordPress site"
- "Update the title of post 123"
- "Activate the Akismet plugin"
- "Show me all admin users"
