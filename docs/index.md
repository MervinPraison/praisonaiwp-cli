---
layout: default
title: PraisonAIWP - AI-Powered WordPress CLI
description: Enterprise-grade WordPress management with AI-powered content generation and automation
---

# PraisonAIWP

**AI-Powered WordPress Content Management CLI Tool**

PraisonAIWP is a comprehensive command-line interface for WordPress management that combines the power of WP-CLI with AI-driven content generation. Designed for developers, agencies, and enterprises who need efficient WordPress site management with intelligent automation.

## ✨ Key Features

### 🤖 AI-Powered Content Generation
- **Auto-publish AI content** with customizable prompts
- **Smart content optimization** for SEO and readability
- **Batch content creation** with consistent quality
- **Integration with OpenAI** for advanced text generation
- **Duplicate detection** with semantic similarity and persistent caching

### 🛠️ Complete WordPress Management
- **50+ CLI commands** covering all WordPress operations
- **Plugin management** (install, activate, update, delete)
- **Theme management** (install, activate, switch, delete)
- **User management** (create, update, delete, role management)
- **Post & Page management** with full CRUD operations
- **Media management** (upload, organize, delete)
- **Database operations** (backup, restore, optimization)

### 🌐 Multi-Transport Connectivity
- **SSH** for remote VPS/VM servers
- **Kubernetes** for K8s-deployed WordPress pods
- **Local execution** for same-server deployments (no SSH needed)
- **Auto-detection** of local mode from config
- **Multi-server configuration** with secure authentication
- **Batch operations** across multiple installations

### 📊 Enterprise Features
- **Multisite management** for WordPress networks
- **Advanced caching** and performance optimization
- **Security management** and monitoring
- **Backup & restore** with scheduling
- **Role-based access control**

## 🚀 Quick Start

### Installation

```bash
# Install via pip
pip install praisonaiwp

# Or install from source
git clone https://github.com/mervinpraison/praisonaiwp.git
cd praisonaiwp
pip install -e .
```

### Basic Usage

```bash
# Initialize configuration
praisonaiwp init

# Add your WordPress server
praisonaiwp config add-server production user@example.com /path/to/wordpress

# Generate AI content and auto-publish
praisonaiwp ai create-post --title "Your Topic" --auto-publish

# List all plugins
praisonaiwp plugin list

# Install a new plugin
praisonaiwp plugin install akismet

# Create a new user
praisonaiwp user create john john@example.com --role editor
```

## 📖 Documentation

- [Installation Guide]({{ '/installation/' | relative_url }})
- [Quick Start Tutorial]({{ '/quickstart/' | relative_url }})
- [Transport Layer]({{ '/transport/' | relative_url }}) — SSH, Kubernetes, and Local
- [Configuration Reference]({{ '/configuration/' | relative_url }})
- [Command Reference]({{ '/commands/' | relative_url }})

## 🏗️ Architecture

PraisonAIWP is built with a modular architecture:

- **Core Engine**: WPClient class for WordPress API interactions
- **Transport Layer**: Pluggable SSH, Kubernetes, and Local transports
- **Configuration System**: Flexible multi-server management
- **AI Integration**: OpenAI-powered content generation
- **CLI Interface**: Human-friendly command structure

## 🔧 Requirements

- Python 3.8+
- WP-CLI installed on target servers (auto-installed if missing)
- SSH access (for remote servers), or `kubectl` (for Kubernetes), or local access
- OpenAI API key (for AI features)

## 📄 License

MIT License - see [LICENSE](https://github.com/mervinpraison/praisonaiwp/blob/main/LICENSE) for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide]({{ '/contributing/' | relative_url }}) for details.

## 📞 Support

- **Documentation**: [Full documentation]({{ '/' | relative_url }})
- **Issues**: [GitHub Issues](https://github.com/mervinpraison/praisonaiwp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mervinpraison/praisonaiwp/discussions)

---

**Built with ❤️ by [Mervin Praison](https://mervinpraison.com)**
