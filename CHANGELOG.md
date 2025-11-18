# Changelog

All notable changes to PraisonAI WPcli will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.15] - 2025-11-18

### Added
- **Advanced Post Creation Options**: Full WP-CLI post create support
  - `--excerpt` - Add post excerpt/summary
  - `--date` - Set custom post date (YYYY-MM-DD HH:MM:SS)
  - `--tags` - Add tags (comma-separated names or IDs)
  - `--meta` - Add custom post meta in JSON format `{"key":"value"}`
  - `--comment-status` - Control comments (open/closed)

### Documentation
- Added comprehensive CLI reference section for AI agents
- Documented all available options for each command
- Added proper quoting examples for multi-word arguments
- Added options summary table
- Included examples for custom meta data, tags, excerpt, and dates

### Notes
- Core `WPClient.create_post()` accepts any WP-CLI parameter via **kwargs
- CLI now exposes the most commonly used advanced options
- Custom taxonomies can be added via `--meta` in JSON format

## [1.0.14] - 2025-11-18

### Added
- **CLI Enhancements**: New options for better post management
  - `--author` option in `create` command - Set post author by user ID or login
  - `--post-content` option in `update` command - Replace entire post content
  - `--post-title` option in `update` command - Update post title
  - `--post-status` option in `update` command - Change post status
  - `--search` / `-s` option in `list` command - Search posts by title/content

### Fixed
- Issue #1: Author can now be set when creating posts via CLI
- Issue #2: Post content can be updated directly without find/replace
- Issue #3: Posts can be searched/filtered in list command

### Testing
- Added 3 test cases verifying core functionality
- All 71/72 tests passing (98.6% pass rate)

### Notes
- Core WPClient already supported these features
- This release adds CLI layer access to existing functionality

## [1.0.13] - 2025-11-17

### Added
- **Generic `wp()` Method**: Universal WP-CLI command executor
  - Supports ALL WP-CLI commands (1000+ commands)
  - Automatic JSON parsing with `format='json'`
  - Underscore to hyphen conversion (dry_run → --dry-run)
  - Boolean flag support (porcelain=True → --porcelain)
  - No need to wait for wrapper methods
  - See GENERIC_WP_METHOD.md for comprehensive guide

### Changed
- Hybrid approach: Keep convenience methods + add generic wp() method
- Users can now use ANY WP-CLI command directly
- Enhanced flexibility for power users

### Testing
- Added 4 new unit tests for wp() method
- All 68/69 tests passing (99% pass rate)

### Documentation
- Added GENERIC_WP_METHOD.md with examples and best practices
- Documented when to use convenience methods vs wp()

## [1.0.12] - 2025-11-17

### Added
- **Term Management**: Complete CRUD operations
  - create_term() - Create new term with options
  - delete_term() - Delete term from taxonomy
  - update_term() - Update term fields
- **Core Commands**: WordPress core information
  - get_core_version() - Get WordPress version
  - core_is_installed() - Check installation status

### Changed
- Updated WPCLI.md with term and core command support
- Enhanced category/term management documentation

### Testing
- Added 5 new unit tests
- All 64/65 tests passing (98% pass rate)

## [1.0.11] - 2025-11-17

### Added
- **Cache Management**: flush_cache(), get_cache_type()
- **Transient Management**: Complete CRUD operations
  - get_transient() - Get transient value
  - set_transient() - Set with optional expiration
  - delete_transient() - Remove transient
- **Menu Management**: Complete menu operations
  - list_menus() - List all menus
  - create_menu() - Create new menu
  - delete_menu() - Remove menu
  - add_menu_item() - Add custom menu item

### Changed
- Updated WPCLI.md with cache, transient, and menu support
- Enhanced summary with all management features

### Testing
- Added 9 new unit tests
- All 59/60 tests passing (98% pass rate)

## [1.0.10] - 2025-11-17

### Added
- **Plugin Activation**: activate_plugin(), deactivate_plugin()
- **Theme Activation**: activate_theme()
- **User Meta Management**: Complete CRUD operations
  - get_user_meta() - Get single or all meta values
  - set_user_meta() - Set meta value
  - update_user_meta() - Update existing meta
  - delete_user_meta() - Remove meta field

### Changed
- Updated WPCLI.md with plugin/theme activation and user meta support
- Enhanced summary with all activation features

### Testing
- Added 7 new unit tests
- All 50/51 tests passing (98% pass rate)

## [1.0.9] - 2025-11-17

### Added
- **Media Management**: import_media() with metadata and post attachment
- **Comment Management**: Complete CRUD operations
  - list_comments() - List comments with filters
  - get_comment() - Get comment details
  - create_comment() - Create comment on post
  - update_comment() - Update comment fields
  - delete_comment() - Delete with force option
  - approve_comment() - Approve comment

### Changed
- Updated WPCLI.md with media and comment support
- Enhanced summary with all management features

### Testing
- Added 8 new unit tests
- All 43/44 tests passing (98% pass rate)

## [1.0.8] - 2025-11-17

### Added
- **User CRUD Operations**: Complete user management
  - create_user() - Create users with role and custom fields
  - update_user() - Update user fields
  - delete_user() - Delete users with post reassignment option
- **Plugin Management**: list_plugins() with status filters
- **Theme Management**: list_themes() with status filters

### Changed
- Updated WPCLI.md with comprehensive user/plugin/theme support
- Enhanced summary section with all management features

### Testing
- Added 5 new unit tests
- All 36/37 tests passing

## [1.0.7] - 2025-11-17

### Added
- **Post Deletion**: delete_post() with force option
- **Post Exists Check**: post_exists() to verify post existence
- **Post Meta Management**: Complete CRUD operations
  - get_post_meta() - Get single or all meta values
  - set_post_meta() - Set meta value
  - update_post_meta() - Update existing meta
  - delete_post_meta() - Remove meta field
- **User Management**: Basic user operations
  - list_users() - List users with filters
  - get_user() - Get user details
- **Option Management**: WordPress options CRUD
  - get_option() - Get option value
  - set_option() - Set option value
  - delete_option() - Remove option

### Changed
- Updated WPCLI.md with comprehensive feature matrix
- Enhanced summary section with all implemented features

### Testing
- Added 15+ new unit tests
- All tests passing (31/31)

## [1.0.6] - 2025-11-17

### Added
- **Fast Search**: Optimized find command with WP_Query 's' parameter
  - Server-side MySQL LIKE search (10x faster)
  - Search 800+ posts in 4 seconds instead of 50+ seconds
  - Only fetches matching posts instead of all posts

### Changed
- Consolidated documentation (removed 10 redundant docs)
- Keep only specialized docs: ARCHITECTURE.md, TESTING.md, CHANGELOG.md
- Enhanced README with category examples and troubleshooting

## [1.0.5] - 2025-11-17

### Added
- **Category Management**: Full category support for WordPress posts
  - New `category` command group with subcommands: set, add, remove, list, search
  - `--category` and `--category-id` options for create and update commands
  - 7 new WPClient methods for category operations
  - Rich table output for category listings
  - Support for both category names and IDs
- **SSH Config Host Integration**: Reference SSH config hosts directly in config.yaml
  - New `ssh_host` parameter to reference `~/.ssh/config` hosts
  - Automatic loading of connection details from SSH config
  - Support for mixing SSH config and direct specification
  - Direct values override SSH config values
- **Enhanced Documentation**: Comprehensive README updates with all features

### Changed
- Updated repository name to PraisonAI-WPcli
- Improved README with category examples and troubleshooting section
- Enhanced configuration flexibility with multiple methods

### Fixed
- Config loading now properly supports both ssh_host and direct specification

## [1.0.4] - 2025-10-26

### Changed
- All examples now use neutral, professional terminology suitable for any WordPress site

## [1.0.3] - 2025-10-26

### Changed
- Updated documentation, examples, and test files with neutral terminology

## [1.0.2] - 2025-10-26

### Documentation
- Updated README.md with comprehensive feature documentation
- Added detailed examples for all new v1.0.1 features
- Enhanced Quick Start guide with auto-install and auto-detect workflows
- Added SSH config integration examples
- Improved feature descriptions with use cases

## [1.0.1] - 2025-10-26

### Added
- **SSH Config Support**: PraisonAIWP now supports `~/.ssh/config` for simplified connection management
  - Use host aliases instead of full connection details
  - Automatically loads username, hostname, port, and SSH key from SSH config
  - Supports advanced SSH features (ProxyJump, ControlMaster, etc.)
  - See `SSH_CONFIG_GUIDE.md` for complete documentation
- **UV Package Manager Support**: Migrated to `uv` for 10-100x faster dependency management
  - Added `pyproject.toml` as primary configuration
  - Added `.python-version` for Python version pinning
  - Created comprehensive `UV_GUIDE.md` documentation
  - Maintained backward compatibility with pip
- **Enhanced Security**: Removed all hardcoded credentials from test files
  - Test scripts now require config file or environment variables
  - Added `.env.example` with placeholder values
  - All documentation uses generic examples

### Changed
- Updated `SSHManager` to support optional parameters (username, key_file)
- SSH config is now loaded automatically by default (can be disabled with `use_ssh_config=False`)
- Improved error messages with helpful guidance for missing configuration

### Fixed
- Fixed `pyproject.toml` requires-python constraint (>=3.8.1 for flake8 compatibility)
- Improved test script configuration loading with better fallbacks

### Documentation
- Added `SSH_CONFIG_GUIDE.md` - Complete guide for SSH config integration
- Added `UV_GUIDE.md` - Comprehensive uv package manager guide
- Added `UV_MIGRATION.md` - Migration documentation and comparison
- Added `TEST_SETUP.md` - Test setup guide with multiple configuration options
- Updated `README.md` with SSH config feature
- Updated `QUICKSTART.md` with SSH config tip
- Added `CHANGELOG.md` - This file

## [1.0.0] - 2025-10-25

### Added
- Initial release of PraisonAIWP
- Core SSH connection management
- WP-CLI wrapper for WordPress operations
- Content editor with line-specific and occurrence-specific replacements
- Configuration management system
- 5 CLI commands: init, create, update, find, list
- Unit tests for core modules
- Node.js parallel executor for bulk operations
- Comprehensive documentation (ARCHITECTURE.md, README.md, QUICKSTART.md)
- Example scripts and files

### Features
- Line-specific text replacement (update line 10 without touching line 55)
- Nth occurrence replacement (update 2nd occurrence only)
- Auto-parallel mode for bulk operations (10x faster)
- Preview mode and dry-run capabilities
- Auto-backup before destructive operations
- Multi-server support
- Smart file format detection (JSON, YAML, CSV)
- Rich CLI output with colors and progress bars

[1.0.1]: https://github.com/MervinPraison/praisonaiwp/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/MervinPraison/praisonaiwp/releases/tag/v1.0.0
