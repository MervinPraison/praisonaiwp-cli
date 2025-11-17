# WP-CLI Commands Reference

## PraisonAI WP Support Status

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp post create** | ✅ | Create new posts |
| **wp post update** | ✅ | Update existing posts |
| **wp post list** | ✅ | List posts with filters |
| **wp post get** | ✅ | Get post details |
| **wp post delete** | ✅ | Delete posts (trash or force) |
| **wp post edit** | ❌ | Launch editor for post |
| **wp post exists** | ✅ | Check if post exists |
| **wp post generate** | ❌ | Generate dummy posts |
| **wp post meta** | ❌ | Manage post meta |
| **wp post term** | ✅ | Manage post terms/categories |
| **wp post url-to-id** | ❌ | Convert URL to post ID |

## Post Parameters (wp post list)

| Parameter | Supported | Feature |
|---|---|---|
| `--post_type` | ✅ | Filter by post type |
| `--post_status` | ✅ | Filter by status (publish, draft, etc) |
| `--s` | ✅ | Search posts (server-side) |
| `--author` | ✅ | Filter by author ID |
| `--author_name` | ✅ | Filter by author name |
| `--cat` | ✅ | Filter by category ID |
| `--category_name` | ✅ | Filter by category slug |
| `--tag` | ✅ | Filter by tag slug |
| `--tag_id` | ✅ | Filter by tag ID |
| `--post__in` | ✅ | Specific post IDs |
| `--post__not_in` | ✅ | Exclude post IDs |
| `--posts_per_page` | ✅ | Limit results |
| `--paged` | ✅ | Pagination |
| `--offset` | ✅ | Skip posts |
| `--order` | ✅ | ASC or DESC |
| `--orderby` | ✅ | Sort by field |
| `--year` | ✅ | Filter by year |
| `--monthnum` | ✅ | Filter by month |
| `--day` | ✅ | Filter by day |
| `--meta_key` | ✅ | Filter by meta key |
| `--meta_value` | ✅ | Filter by meta value |
| `--meta_compare` | ✅ | Meta comparison operator |
| `--fields` | ✅ | Limit output fields |
| `--format` | ✅ | Output format (json, csv, table) |

## Term/Category Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp term create** | ❌ | Create new term |
| **wp term delete** | ❌ | Delete term |
| **wp term list** | ✅ | List terms in taxonomy |
| **wp term get** | ✅ | Get term details |
| **wp term update** | ❌ | Update term |
| **wp term meta** | ❌ | Manage term meta |
| **wp term migrate** | ❌ | Migrate term to another taxonomy |
| **wp term recount** | ❌ | Recount term posts |
| **wp post term add** | ✅ | Add term to post |
| **wp post term remove** | ✅ | Remove term from post |
| **wp post term list** | ✅ | List post terms |
| **wp post term set** | ✅ | Set post terms (replace all) |

## Database Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp db query** | ✅ | Execute SQL query |
| **wp db export** | ❌ | Export database |
| **wp db import** | ❌ | Import database |
| **wp db optimize** | ❌ | Optimize database |
| **wp db repair** | ❌ | Repair database |
| **wp db reset** | ❌ | Reset database |
| **wp db search** | ❌ | Search database |
| **wp db tables** | ❌ | List database tables |

## Search & Replace

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp search-replace** | ✅ | Search and replace in database |
| **--dry-run** | ✅ | Preview changes |
| **--precise** | ❌ | Match whole words only |
| **--regex** | ❌ | Use regex patterns |
| **--all-tables** | ❌ | Include all tables |

## Core Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp core version** | ❌ | Check WP version |
| **wp core update** | ❌ | Update WordPress |
| **wp core download** | ❌ | Download WordPress |
| **wp core install** | ❌ | Install WordPress |
| **wp core is-installed** | ❌ | Check if WP is installed |

## Plugin Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp plugin list** | ❌ | List plugins |
| **wp plugin install** | ❌ | Install plugin |
| **wp plugin activate** | ❌ | Activate plugin |
| **wp plugin deactivate** | ❌ | Deactivate plugin |
| **wp plugin delete** | ❌ | Delete plugin |
| **wp plugin update** | ❌ | Update plugin |

## Theme Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp theme list** | ❌ | List themes |
| **wp theme install** | ❌ | Install theme |
| **wp theme activate** | ❌ | Activate theme |
| **wp theme delete** | ❌ | Delete theme |
| **wp theme update** | ❌ | Update theme |

## User Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp user list** | ❌ | List users |
| **wp user create** | ❌ | Create user |
| **wp user update** | ❌ | Update user |
| **wp user delete** | ❌ | Delete user |
| **wp user meta** | ❌ | Manage user meta |

## Option Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp option get** | ❌ | Get option value |
| **wp option set** | ❌ | Set option value |
| **wp option delete** | ❌ | Delete option |
| **wp option list** | ❌ | List options |

## Media Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp media import** | ❌ | Import media |
| **wp media regenerate** | ❌ | Regenerate thumbnails |

## Comment Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp comment list** | ❌ | List comments |
| **wp comment create** | ❌ | Create comment |
| **wp comment delete** | ❌ | Delete comment |
| **wp comment approve** | ❌ | Approve comment |
| **wp comment spam** | ❌ | Mark as spam |

## Menu Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp menu list** | ❌ | List menus |
| **wp menu create** | ❌ | Create menu |
| **wp menu item add** | ❌ | Add menu item |

## Cache Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp cache flush** | ❌ | Flush cache |
| **wp cache type** | ❌ | Get cache type |

## Transient Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp transient delete** | ❌ | Delete transient |
| **wp transient get** | ❌ | Get transient |
| **wp transient set** | ❌ | Set transient |

## Cron Commands

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp cron event list** | ❌ | List cron events |
| **wp cron event run** | ❌ | Run cron event |

## Export/Import

| WP-CLI Command | Supported | Feature |
|---|---|---|
| **wp export** | ❌ | Export content |
| **wp import** | ❌ | Import content |

## Summary

### Currently Supported (✅)
- Post create, update, list, get
- Post search with WP_Query parameters
- Category/term management (set, add, remove, list)
- Database queries
- Search and replace
- All WP_Query parameters via `wp post list`

### Not Supported (❌)
- Post deletion
- Post meta management
- Plugin/theme management
- User management
- Core WordPress management
- Media management
- Comment management
- Menu management
- Cache/transient management
- Cron management
- Export/import

### Implementation Priority
1. Post meta management
2. Post deletion
3. User management
4. Plugin/theme listing
5. Option management
