"""WordPress CLI client for PraisonAIWP"""

import json
from typing import Any, Optional, Dict, List
from praisonaiwp.core.ssh_manager import SSHManager
from praisonaiwp.utils.logger import get_logger
from praisonaiwp.utils.exceptions import WPCLIError

logger = get_logger(__name__)


class WPClient:
    """WordPress CLI operations wrapper"""
    
    def __init__(
        self,
        ssh: SSHManager,
        wp_path: str,
        php_bin: str = 'php',
        wp_cli: str = '/usr/local/bin/wp',
        verify_installation: bool = True
    ):
        """
        Initialize WP Client
        
        Args:
            ssh: SSH Manager instance
            wp_path: WordPress installation path
            php_bin: PHP binary path (default: 'php')
            wp_cli: WP-CLI binary path (default: '/usr/local/bin/wp')
            verify_installation: Verify WP-CLI and WordPress are available (default: True)
        """
        self.ssh = ssh
        self.wp_path = wp_path
        self.php_bin = php_bin
        self.wp_cli = wp_cli
        
        logger.debug(f"Initialized WPClient for {wp_path}")
        
        # Verify installation if requested
        if verify_installation:
            self._verify_installation()
    
    def _verify_installation(self):
        """
        Verify WP-CLI and WordPress installation
        
        Raises:
            WPCLIError: If WP-CLI or WordPress not found
        """
        try:
            # Check if WP-CLI binary exists
            stdout, stderr = self.ssh.execute(f"test -f {self.wp_cli} && echo 'exists' || echo 'not found'")
            
            if 'not found' in stdout:
                raise WPCLIError(
                    f"WP-CLI not found at {self.wp_cli}\n"
                    f"\nInstallation instructions:\n"
                    f"1. Download: curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar\n"
                    f"2. Make executable: chmod +x wp-cli.phar\n"
                    f"3. Move to path: sudo mv wp-cli.phar {self.wp_cli}\n"
                    f"\nOr specify correct path with --wp-cli option"
                )
            
            # Check if WordPress directory exists
            stdout, stderr = self.ssh.execute(f"test -d {self.wp_path} && echo 'exists' || echo 'not found'")
            
            if 'not found' in stdout:
                raise WPCLIError(
                    f"WordPress installation not found at {self.wp_path}\n"
                    f"Please verify the WordPress path is correct."
                )
            
            # Check if wp-config.php exists
            stdout, stderr = self.ssh.execute(f"test -f {self.wp_path}/wp-config.php && echo 'exists' || echo 'not found'")
            
            if 'not found' in stdout:
                raise WPCLIError(
                    f"wp-config.php not found in {self.wp_path}\n"
                    f"This doesn't appear to be a valid WordPress installation."
                )
            
            # Test WP-CLI execution
            stdout, stderr = self.ssh.execute(f"cd {self.wp_path} && {self.php_bin} {self.wp_cli} --version")
            
            if stderr and ('command not found' in stderr.lower() or 'no such file' in stderr.lower()):
                raise WPCLIError(
                    f"Failed to execute WP-CLI\n"
                    f"Error: {stderr}\n"
                    f"\nPossible issues:\n"
                    f"1. PHP binary not found: {self.php_bin}\n"
                    f"2. WP-CLI not executable: {self.wp_cli}\n"
                    f"3. Missing PHP extensions (mysql, mysqli)\n"
                    f"\nFor Plesk servers, try: /opt/plesk/php/8.3/bin/php"
                )
            
            if 'WP-CLI' in stdout:
                logger.info(f"WP-CLI verified: {stdout.strip()}")
            else:
                logger.warning(f"WP-CLI verification returned unexpected output: {stdout}")
        
        except WPCLIError:
            raise
        except Exception as e:
            logger.warning(f"Could not verify WP-CLI installation: {e}")
    
    def _execute_wp(self, command: str) -> str:
        """
        Execute WP-CLI command
        
        Args:
            command: WP-CLI command (without 'wp' prefix)
            
        Returns:
            Command output
            
        Raises:
            WPCLIError: If command fails
        """
        full_cmd = f"cd {self.wp_path} && {self.php_bin} {self.wp_cli} {command}"
        
        logger.debug(f"Executing WP-CLI: {command}")
        
        try:
            stdout, stderr = self.ssh.execute(full_cmd)
        except Exception as e:
            raise WPCLIError(f"Failed to execute WP-CLI command: {e}")
        
        # Check for common error patterns
        if stderr:
            error_lower = stderr.lower()
            
            if 'command not found' in error_lower:
                raise WPCLIError(
                    f"WP-CLI command not found\n"
                    f"Error: {stderr}\n"
                    f"\nPlease verify:\n"
                    f"1. WP-CLI is installed at: {self.wp_cli}\n"
                    f"2. PHP binary is correct: {self.php_bin}"
                )
            
            if 'no such file or directory' in error_lower:
                raise WPCLIError(
                    f"File or directory not found\n"
                    f"Error: {stderr}\n"
                    f"\nPlease verify:\n"
                    f"1. WordPress path: {self.wp_path}\n"
                    f"2. WP-CLI path: {self.wp_cli}"
                )
            
            if 'error:' in error_lower:
                logger.error(f"WP-CLI error: {stderr}")
                raise WPCLIError(f"WP-CLI error: {stderr}")
        
        return stdout.strip()
    
    def get_post(self, post_id: int, field: Optional[str] = None) -> Any:
        """
        Get post data
        
        Args:
            post_id: Post ID
            field: Specific field to retrieve (optional)
            
        Returns:
            Post data (dict if no field specified, str if field specified)
        """
        cmd = f"post get {post_id}"
        
        if field:
            cmd += f" --field={field}"
            result = self._execute_wp(cmd)
            return result
        else:
            cmd += " --format=json"
            result = self._execute_wp(cmd)
            return json.loads(result)
    
    def create_post(self, **kwargs) -> int:
        """
        Create a new post
        
        Args:
            **kwargs: Post fields (post_title, post_content, post_status, etc.)
            
        Returns:
            Created post ID
        """
        args = []
        for key, value in kwargs.items():
            # Escape single quotes in value
            escaped_value = str(value).replace("'", "'\\''")
            args.append(f"--{key}='{escaped_value}'")
        
        cmd = f"post create {' '.join(args)} --porcelain"
        result = self._execute_wp(cmd)
        
        post_id = int(result.strip())
        logger.info(f"Created post ID: {post_id}")
        
        return post_id
    
    def update_post(self, post_id: int, **kwargs) -> bool:
        """
        Update an existing post
        
        Args:
            post_id: Post ID to update
            **kwargs: Fields to update
            
        Returns:
            True if successful
        """
        args = []
        for key, value in kwargs.items():
            # Escape single quotes in value
            escaped_value = str(value).replace("'", "'\\''")
            args.append(f"--{key}='{escaped_value}'")
        
        cmd = f"post update {post_id} {' '.join(args)}"
        self._execute_wp(cmd)
        
        logger.info(f"Updated post ID: {post_id}")
        return True
    
    def delete_post(self, post_id: int, force: bool = False) -> bool:
        """
        Delete a post
        
        Args:
            post_id: Post ID to delete
            force: Skip trash and force deletion
            
        Returns:
            True if successful
        """
        force_flag = '--force' if force else ''
        cmd = f"post delete {post_id} {force_flag}"
        self._execute_wp(cmd)
        
        logger.info(f"Deleted post ID: {post_id}")
        return True
    
    def post_exists(self, post_id: int) -> bool:
        """
        Check if a post exists
        
        Args:
            post_id: Post ID to check
            
        Returns:
            True if post exists, False otherwise
        """
        try:
            cmd = f"post exists {post_id}"
            self._execute_wp(cmd)
            logger.debug(f"Post {post_id} exists")
            return True
        except WPCLIError:
            logger.debug(f"Post {post_id} does not exist")
            return False
    
    def get_post_meta(self, post_id: int, key: str = None) -> Any:
        """
        Get post meta value(s)
        
        Args:
            post_id: Post ID
            key: Meta key (if None, returns all meta)
            
        Returns:
            Meta value or dict of all meta
        """
        if key:
            cmd = f"post meta get {post_id} {key}"
            result = self._execute_wp(cmd)
            return result.strip()
        else:
            cmd = f"post meta list {post_id} --format=json"
            result = self._execute_wp(cmd)
            return json.loads(result)
    
    def set_post_meta(self, post_id: int, key: str, value: str) -> bool:
        """
        Set post meta value
        
        Args:
            post_id: Post ID
            key: Meta key
            value: Meta value
            
        Returns:
            True if successful
        """
        escaped_value = str(value).replace("'", "'\\''")
        cmd = f"post meta set {post_id} {key} '{escaped_value}'"
        self._execute_wp(cmd)
        logger.info(f"Set meta {key} for post {post_id}")
        return True
    
    def delete_post_meta(self, post_id: int, key: str) -> bool:
        """
        Delete post meta
        
        Args:
            post_id: Post ID
            key: Meta key
            
        Returns:
            True if successful
        """
        cmd = f"post meta delete {post_id} {key}"
        self._execute_wp(cmd)
        logger.info(f"Deleted meta {key} from post {post_id}")
        return True
    
    def update_post_meta(self, post_id: int, key: str, value: str) -> bool:
        """
        Update post meta value
        
        Args:
            post_id: Post ID
            key: Meta key
            value: Meta value
            
        Returns:
            True if successful
        """
        escaped_value = str(value).replace("'", "'\\''")
        cmd = f"post meta update {post_id} {key} '{escaped_value}'"
        self._execute_wp(cmd)
        logger.info(f"Updated meta {key} for post {post_id}")
        return True
    
    def list_users(self, **filters) -> List[Dict[str, Any]]:
        """
        List users with filters
        
        Args:
            **filters: Filters (role, search, etc.)
            
        Returns:
            List of user dictionaries
        """
        args = ["--format=json"]
        
        for key, value in filters.items():
            args.append(f"--{key}={value}")
        
        cmd = f"user list {' '.join(args)}"
        result = self._execute_wp(cmd)
        
        return json.loads(result)
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Get user details
        
        Args:
            user_id: User ID
            
        Returns:
            User dictionary
        """
        cmd = f"user get {user_id} --format=json"
        result = self._execute_wp(cmd)
        
        return json.loads(result)
    
    def create_user(self, username: str, email: str, **kwargs) -> int:
        """
        Create a new user
        
        Args:
            username: Username
            email: Email address
            **kwargs: Additional user fields (role, user_pass, display_name, etc.)
            
        Returns:
            User ID
        """
        args = [username, email]
        
        for key, value in kwargs.items():
            escaped_value = str(value).replace("'", "'\\''")
            args.append(f"--{key}='{escaped_value}'")
        
        cmd = f"user create {' '.join(args)} --porcelain"
        result = self._execute_wp(cmd)
        user_id = int(result.strip())
        logger.info(f"Created user {username} with ID {user_id}")
        return user_id
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """
        Update user fields
        
        Args:
            user_id: User ID
            **kwargs: User fields to update
            
        Returns:
            True if successful
        """
        args = [str(user_id)]
        
        for key, value in kwargs.items():
            escaped_value = str(value).replace("'", "'\\''")
            args.append(f"--{key}='{escaped_value}'")
        
        cmd = f"user update {' '.join(args)}"
        self._execute_wp(cmd)
        logger.info(f"Updated user {user_id}")
        return True
    
    def delete_user(self, user_id: int, reassign: int = None) -> bool:
        """
        Delete a user
        
        Args:
            user_id: User ID to delete
            reassign: User ID to reassign posts to (optional)
            
        Returns:
            True if successful
        """
        args = [str(user_id), "--yes"]
        
        if reassign is not None:
            args.append(f"--reassign={reassign}")
        
        cmd = f"user delete {' '.join(args)}"
        self._execute_wp(cmd)
        logger.info(f"Deleted user {user_id}")
        return True
    
    def get_option(self, option_name: str) -> str:
        """
        Get WordPress option value
        
        Args:
            option_name: Option name
            
        Returns:
            Option value
        """
        cmd = f"option get {option_name}"
        result = self._execute_wp(cmd)
        
        return result.strip()
    
    def set_option(self, option_name: str, value: str) -> bool:
        """
        Set WordPress option value
        
        Args:
            option_name: Option name
            value: Option value
            
        Returns:
            True if successful
        """
        escaped_value = str(value).replace("'", "'\\''")
        cmd = f"option set {option_name} '{escaped_value}'"
        self._execute_wp(cmd)
        logger.info(f"Set option {option_name}")
        return True
    
    def delete_option(self, option_name: str) -> bool:
        """
        Delete WordPress option
        
        Args:
            option_name: Option name
            
        Returns:
            True if successful
        """
        cmd = f"option delete {option_name}"
        self._execute_wp(cmd)
        logger.info(f"Deleted option {option_name}")
        return True
    
    def list_plugins(self, **filters) -> List[Dict[str, Any]]:
        """
        List installed plugins
        
        Args:
            **filters: Filters (status, etc.)
            
        Returns:
            List of plugin dictionaries
        """
        args = ["--format=json"]
        
        for key, value in filters.items():
            args.append(f"--{key}={value}")
        
        cmd = f"plugin list {' '.join(args)}"
        result = self._execute_wp(cmd)
        
        return json.loads(result)
    
    def list_themes(self, **filters) -> List[Dict[str, Any]]:
        """
        List installed themes
        
        Args:
            **filters: Filters (status, etc.)
            
        Returns:
            List of theme dictionaries
        """
        args = ["--format=json"]
        
        for key, value in filters.items():
            args.append(f"--{key}={value}")
        
        cmd = f"theme list {' '.join(args)}"
        result = self._execute_wp(cmd)
        
        return json.loads(result)
    
    def activate_plugin(self, plugin: str) -> bool:
        """
        Activate a plugin
        
        Args:
            plugin: Plugin slug or path
            
        Returns:
            True if successful
        """
        cmd = f"plugin activate {plugin}"
        self._execute_wp(cmd)
        logger.info(f"Activated plugin {plugin}")
        return True
    
    def deactivate_plugin(self, plugin: str) -> bool:
        """
        Deactivate a plugin
        
        Args:
            plugin: Plugin slug or path
            
        Returns:
            True if successful
        """
        cmd = f"plugin deactivate {plugin}"
        self._execute_wp(cmd)
        logger.info(f"Deactivated plugin {plugin}")
        return True
    
    def activate_theme(self, theme: str) -> bool:
        """
        Activate a theme
        
        Args:
            theme: Theme slug
            
        Returns:
            True if successful
        """
        cmd = f"theme activate {theme}"
        self._execute_wp(cmd)
        logger.info(f"Activated theme {theme}")
        return True
    
    def get_user_meta(self, user_id: int, key: str = None) -> Any:
        """
        Get user meta value(s)
        
        Args:
            user_id: User ID
            key: Meta key (optional, returns all if not specified)
            
        Returns:
            Meta value or list of all meta
        """
        if key:
            cmd = f"user meta get {user_id} {key}"
            result = self._execute_wp(cmd)
            return result.strip()
        else:
            cmd = f"user meta list {user_id} --format=json"
            result = self._execute_wp(cmd)
            return json.loads(result)
    
    def set_user_meta(self, user_id: int, key: str, value: str) -> bool:
        """
        Set user meta value
        
        Args:
            user_id: User ID
            key: Meta key
            value: Meta value
            
        Returns:
            True if successful
        """
        escaped_value = str(value).replace("'", "'\\''")
        cmd = f"user meta add {user_id} {key} '{escaped_value}'"
        self._execute_wp(cmd)
        logger.info(f"Set meta {key} for user {user_id}")
        return True
    
    def update_user_meta(self, user_id: int, key: str, value: str) -> bool:
        """
        Update user meta value
        
        Args:
            user_id: User ID
            key: Meta key
            value: Meta value
            
        Returns:
            True if successful
        """
        escaped_value = str(value).replace("'", "'\\''")
        cmd = f"user meta update {user_id} {key} '{escaped_value}'"
        self._execute_wp(cmd)
        logger.info(f"Updated meta {key} for user {user_id}")
        return True
    
    def delete_user_meta(self, user_id: int, key: str) -> bool:
        """
        Delete user meta
        
        Args:
            user_id: User ID
            key: Meta key
            
        Returns:
            True if successful
        """
        cmd = f"user meta delete {user_id} {key}"
        self._execute_wp(cmd)
        logger.info(f"Deleted meta {key} for user {user_id}")
        return True
    
    def import_media(self, file_path: str, post_id: int = None, **kwargs) -> int:
        """
        Import media file to WordPress
        
        Args:
            file_path: Path to media file
            post_id: Post ID to attach to (optional)
            **kwargs: Additional options (title, caption, alt, desc, etc.)
            
        Returns:
            Attachment ID
        """
        args = [f"'{file_path}'"]
        
        if post_id is not None:
            args.append(f"--post_id={post_id}")
        
        for key, value in kwargs.items():
            escaped_value = str(value).replace("'", "'\\''")
            args.append(f"--{key}='{escaped_value}'")
        
        args.append("--porcelain")
        
        cmd = f"media import {' '.join(args)}"
        result = self._execute_wp(cmd)
        attachment_id = int(result.strip())
        logger.info(f"Imported media {file_path} with ID {attachment_id}")
        return attachment_id
    
    def list_comments(self, **filters) -> List[Dict[str, Any]]:
        """
        List comments with filters
        
        Args:
            **filters: Filters (status, post_id, etc.)
            
        Returns:
            List of comment dictionaries
        """
        args = ["--format=json"]
        
        for key, value in filters.items():
            args.append(f"--{key}={value}")
        
        cmd = f"comment list {' '.join(args)}"
        result = self._execute_wp(cmd)
        
        return json.loads(result)
    
    def get_comment(self, comment_id: int) -> Dict[str, Any]:
        """
        Get comment details
        
        Args:
            comment_id: Comment ID
            
        Returns:
            Comment dictionary
        """
        cmd = f"comment get {comment_id} --format=json"
        result = self._execute_wp(cmd)
        
        return json.loads(result)
    
    def create_comment(self, post_id: int, **kwargs) -> int:
        """
        Create a new comment
        
        Args:
            post_id: Post ID
            **kwargs: Comment fields (comment_content, comment_author, etc.)
            
        Returns:
            Comment ID
        """
        args = [str(post_id)]
        
        for key, value in kwargs.items():
            escaped_value = str(value).replace("'", "'\\''")
            args.append(f"--{key}='{escaped_value}'")
        
        args.append("--porcelain")
        
        cmd = f"comment create {' '.join(args)}"
        result = self._execute_wp(cmd)
        comment_id = int(result.strip())
        logger.info(f"Created comment {comment_id} on post {post_id}")
        return comment_id
    
    def update_comment(self, comment_id: int, **kwargs) -> bool:
        """
        Update comment fields
        
        Args:
            comment_id: Comment ID
            **kwargs: Comment fields to update
            
        Returns:
            True if successful
        """
        args = [str(comment_id)]
        
        for key, value in kwargs.items():
            escaped_value = str(value).replace("'", "'\\''")
            args.append(f"--{key}='{escaped_value}'")
        
        cmd = f"comment update {' '.join(args)}"
        self._execute_wp(cmd)
        logger.info(f"Updated comment {comment_id}")
        return True
    
    def delete_comment(self, comment_id: int, force: bool = False) -> bool:
        """
        Delete a comment
        
        Args:
            comment_id: Comment ID
            force: Bypass trash and force deletion
            
        Returns:
            True if successful
        """
        args = [str(comment_id)]
        
        if force:
            args.append("--force")
        
        cmd = f"comment delete {' '.join(args)}"
        self._execute_wp(cmd)
        logger.info(f"Deleted comment {comment_id}")
        return True
    
    def approve_comment(self, comment_id: int) -> bool:
        """
        Approve a comment
        
        Args:
            comment_id: Comment ID
            
        Returns:
            True if successful
        """
        cmd = f"comment approve {comment_id}"
        self._execute_wp(cmd)
        logger.info(f"Approved comment {comment_id}")
        return True
    
    def list_posts(
        self,
        post_type: str = 'post',
        **filters
    ) -> List[Dict[str, Any]]:
        """
        List posts with filters
        
        Args:
            post_type: Post type (default: 'post')
            **filters: Additional filters (post_status, etc.)
            
        Returns:
            List of post dictionaries
        """
        args = [f"--post_type={post_type}", "--format=json"]
        
        for key, value in filters.items():
            args.append(f"--{key}={value}")
        
        cmd = f"post list {' '.join(args)}"
        result = self._execute_wp(cmd)
        
        return json.loads(result)
    
    def db_query(self, query: str) -> str:
        """
        Execute database query
        
        Args:
            query: SQL query
            
        Returns:
            Query result as JSON string
        """
        # Escape query for shell
        escaped_query = query.replace('"', '\\"').replace('$', '\\$')
        cmd = f'db query "{escaped_query}" --format=json'
        
        return self._execute_wp(cmd)
    
    def search_replace(
        self,
        old: str,
        new: str,
        tables: Optional[List[str]] = None,
        dry_run: bool = False
    ) -> str:
        """
        Search and replace in database
        
        Args:
            old: Text to find
            new: Replacement text
            tables: Tables to search (optional)
            dry_run: Preview changes without applying
            
        Returns:
            Command output
        """
        cmd = f"search-replace '{old}' '{new}'"
        
        if tables:
            cmd += f" {' '.join(tables)}"
        
        if dry_run:
            cmd += " --dry-run"
        
        return self._execute_wp(cmd)
    
    def set_post_categories(self, post_id: int, category_ids: List[int]) -> bool:
        """
        Set post categories (replace all existing)
        
        Args:
            post_id: Post ID
            category_ids: List of category IDs
            
        Returns:
            True if successful
        """
        if not category_ids:
            logger.warning("No category IDs provided")
            return False
        
        # Join category IDs with comma
        cat_ids_str = ','.join(map(str, category_ids))
        cmd = f"post update {post_id} --post_category={cat_ids_str}"
        
        self._execute_wp(cmd)
        logger.info(f"Set categories {cat_ids_str} for post {post_id}")
        
        return True
    
    def add_post_category(self, post_id: int, category_id: int) -> bool:
        """
        Add a category to post (append)
        
        Args:
            post_id: Post ID
            category_id: Category ID to add
            
        Returns:
            True if successful
        """
        cmd = f"post term add {post_id} category {category_id}"
        
        self._execute_wp(cmd)
        logger.info(f"Added category {category_id} to post {post_id}")
        
        return True
    
    def remove_post_category(self, post_id: int, category_id: int) -> bool:
        """
        Remove a category from post
        
        Args:
            post_id: Post ID
            category_id: Category ID to remove
            
        Returns:
            True if successful
        """
        cmd = f"post term remove {post_id} category {category_id}"
        
        self._execute_wp(cmd)
        logger.info(f"Removed category {category_id} from post {post_id}")
        
        return True
    
    def list_categories(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all categories
        
        Args:
            search: Optional search query
            
        Returns:
            List of category dictionaries
        """
        cmd = "term list category --format=json --fields=term_id,name,slug,parent,count"
        
        if search:
            escaped_search = search.replace('"', '\\"')
            cmd += f' --search="{escaped_search}"'
        
        result = self._execute_wp(cmd)
        categories = json.loads(result)
        
        logger.debug(f"Found {len(categories)} categories")
        return categories
    
    def get_post_categories(self, post_id: int) -> List[Dict[str, Any]]:
        """
        Get categories for a specific post
        
        Args:
            post_id: Post ID
            
        Returns:
            List of category dictionaries
        """
        cmd = f"post term list {post_id} category --format=json --fields=term_id,name,slug,parent"
        
        result = self._execute_wp(cmd)
        categories = json.loads(result)
        
        logger.debug(f"Post {post_id} has {len(categories)} categories")
        return categories
    
    def get_category_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get category by name or slug
        
        Args:
            name: Category name or slug
            
        Returns:
            Category dictionary or None
        """
        try:
            # Try to get by slug first
            cmd = f"term get category '{name}' --format=json --fields=term_id,name,slug,parent"
            result = self._execute_wp(cmd)
            category = json.loads(result)
            
            logger.debug(f"Found category: {category}")
            return category
        except WPCLIError:
            # If not found by slug, search by name
            categories = self.list_categories(search=name)
            
            # Find exact match (case-insensitive)
            for cat in categories:
                if cat['name'].lower() == name.lower() or cat['slug'].lower() == name.lower():
                    return cat
            
            logger.warning(f"Category '{name}' not found")
            return None
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """
        Get category by ID
        
        Args:
            category_id: Category ID
            
        Returns:
            Category dictionary or None
        """
        try:
            cmd = f"term get category {category_id} --format=json --fields=term_id,name,slug,parent"
            result = self._execute_wp(cmd)
            category = json.loads(result)
            
            logger.debug(f"Found category: {category}")
            return category
        except WPCLIError:
            logger.warning(f"Category ID {category_id} not found")
            return None
