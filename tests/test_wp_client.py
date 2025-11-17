"""Tests for WPClient (with mocking)"""

import pytest
from unittest.mock import Mock, MagicMock
from praisonaiwp.core.wp_client import WPClient
from praisonaiwp.utils.exceptions import WPCLIError


class TestWPClient:
    """Test WPClient functionality"""
    
    @pytest.fixture
    def mock_ssh(self):
        """Create mock SSH manager"""
        ssh = Mock()
        ssh.execute = Mock(return_value=("output", ""))
        return ssh
    
    @pytest.fixture
    def wp_client(self, mock_ssh):
        """Create WP client with mock SSH"""
        return WPClient(
            ssh=mock_ssh,
            wp_path="/var/www/html",
            php_bin="php",
            wp_cli="/usr/local/bin/wp"
        )
    
    def test_execute_wp_success(self, wp_client, mock_ssh):
        """Test successful WP-CLI execution"""
        mock_ssh.execute.return_value = ("Success", "")
        
        result = wp_client._execute_wp("post list")
        
        assert result == "Success"
        mock_ssh.execute.assert_called_once()
    
    def test_execute_wp_error(self, wp_client, mock_ssh):
        """Test WP-CLI execution with error"""
        mock_ssh.execute.return_value = ("", "Error: Something went wrong")
        
        with pytest.raises(WPCLIError):
            wp_client._execute_wp("post list")
    
    def test_get_post_with_field(self, wp_client, mock_ssh):
        """Test getting specific post field"""
        mock_ssh.execute.return_value = ("Post content here", "")
        
        content = wp_client.get_post(123, field='post_content')
        
        assert content == "Post content here"
        assert "post get 123 --field=post_content" in mock_ssh.execute.call_args[0][0]
    
    def test_get_post_json(self, wp_client, mock_ssh):
        """Test getting post as JSON"""
        import json
        post_data = {"ID": 123, "post_title": "Test"}
        mock_ssh.execute.return_value = (json.dumps(post_data), "")
        
        result = wp_client.get_post(123)
        
        assert result == post_data
        assert "--format=json" in mock_ssh.execute.call_args[0][0]
    
    def test_create_post(self, wp_client, mock_ssh):
        """Test creating post"""
        mock_ssh.execute.return_value = ("456", "")
        
        post_id = wp_client.create_post(
            post_title="Test Post",
            post_content="Content",
            post_status="publish"
        )
        
        assert post_id == 456
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post create" in call_args
        assert "--porcelain" in call_args
    
    def test_update_post(self, wp_client, mock_ssh):
        """Test updating post"""
        mock_ssh.execute.return_value = ("Success", "")
        
        result = wp_client.update_post(
            123,
            post_title="Updated Title"
        )
        
        assert result is True
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post update 123" in call_args
    
    def test_list_posts(self, wp_client, mock_ssh):
        """Test listing posts"""
        import json
        posts = [{"ID": 1, "post_title": "Post 1"}]
        mock_ssh.execute.return_value = (json.dumps(posts), "")
        
        result = wp_client.list_posts(post_type='page')
        
        assert result == posts
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post list" in call_args
        assert "--post_type=page" in call_args
    
    def test_db_query(self, wp_client, mock_ssh):
        """Test database query"""
        mock_ssh.execute.return_value = ("Query result", "")
        
        result = wp_client.db_query("SELECT * FROM wp_posts")
        
        assert result == "Query result"
        call_args = mock_ssh.execute.call_args[0][0]
        assert "db query" in call_args
    
    def test_delete_post(self, wp_client, mock_ssh):
        """Test delete post"""
        mock_ssh.execute.return_value = ("Success: Trashed post 123.", "")
        
        result = wp_client.delete_post(123)
        
        assert result is True
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post delete 123" in call_args
    
    def test_delete_post_force(self, wp_client, mock_ssh):
        """Test force delete post"""
        mock_ssh.execute.return_value = ("Success: Deleted post 123.", "")
        
        result = wp_client.delete_post(123, force=True)
        
        assert result is True
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post delete 123 --force" in call_args
    
    def test_post_exists_true(self, wp_client, mock_ssh):
        """Test post exists returns True"""
        mock_ssh.execute.return_value = ("", "")
        
        result = wp_client.post_exists(123)
        
        assert result is True
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post exists 123" in call_args
    
    def test_post_exists_false(self, wp_client, mock_ssh):
        """Test post exists returns False"""
        from praisonaiwp.utils.exceptions import WPCLIError
        mock_ssh.execute.side_effect = WPCLIError("Post does not exist")
        
        result = wp_client.post_exists(999)
        
        assert result is False
    
    def test_search_replace(self, wp_client, mock_ssh):
        """Test search and replace"""
        mock_ssh.execute.return_value = ("Replaced 5 occurrences", "")
        
        result = wp_client.search_replace("old", "new", dry_run=True)
        
        assert "Replaced" in result
        call_args = mock_ssh.execute.call_args[0][0]
        assert "search-replace" in call_args
        assert "--dry-run" in call_args
    
    def test_create_post_escapes_quotes(self, wp_client, mock_ssh):
        """Test that single quotes are properly escaped"""
        mock_ssh.execute.return_value = ("123", "")
        
        wp_client.create_post(
            post_title="Post with 'quotes'",
            post_content="Content with 'quotes'"
        )
        
        call_args = mock_ssh.execute.call_args[0][0]
        # Should escape single quotes
        assert "'\\''" in call_args or "\\'" in call_args
    
    def test_set_post_categories(self, wp_client, mock_ssh):
        """Test setting post categories"""
        mock_ssh.execute.return_value = ("Success", "")
        
        result = wp_client.set_post_categories(123, [1, 2, 3])
        
        assert result is True
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post update 123" in call_args
        assert "--post_category=1,2,3" in call_args
    
    def test_add_post_category(self, wp_client, mock_ssh):
        """Test adding a category to post"""
        mock_ssh.execute.return_value = ("Success", "")
        
        result = wp_client.add_post_category(123, 5)
        
        assert result is True
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post term add 123 category 5" in call_args
    
    def test_remove_post_category(self, wp_client, mock_ssh):
        """Test removing a category from post"""
        mock_ssh.execute.return_value = ("Success", "")
        
        result = wp_client.remove_post_category(123, 1)
        
        assert result is True
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post term remove 123 category 1" in call_args
    
    def test_list_categories(self, wp_client, mock_ssh):
        """Test listing categories"""
        import json
        categories = [
            {"term_id": "1", "name": "Uncategorized", "slug": "uncategorized", "parent": "0", "count": "5"},
            {"term_id": "2", "name": "News", "slug": "news", "parent": "0", "count": "10"}
        ]
        mock_ssh.execute.return_value = (json.dumps(categories), "")
        
        result = wp_client.list_categories()
        
        assert result == categories
        call_args = mock_ssh.execute.call_args[0][0]
        assert "term list category" in call_args
        assert "--format=json" in call_args
    
    def test_list_categories_with_search(self, wp_client, mock_ssh):
        """Test searching categories"""
        import json
        categories = [{"term_id": "2", "name": "News", "slug": "news", "parent": "0", "count": "10"}]
        mock_ssh.execute.return_value = (json.dumps(categories), "")
        
        result = wp_client.list_categories(search="News")
        
        assert result == categories
        call_args = mock_ssh.execute.call_args[0][0]
        assert "term list category" in call_args
        assert '--search="News"' in call_args
    
    def test_get_post_categories(self, wp_client, mock_ssh):
        """Test getting categories for a post"""
        import json
        categories = [
            {"term_id": "1", "name": "Uncategorized", "slug": "uncategorized", "parent": "0"},
            {"term_id": "2", "name": "News", "slug": "news", "parent": "0"}
        ]
        mock_ssh.execute.return_value = (json.dumps(categories), "")
        
        result = wp_client.get_post_categories(123)
        
        assert result == categories
        call_args = mock_ssh.execute.call_args[0][0]
        assert "post term list 123 category" in call_args
    
    def test_get_category_by_name(self, wp_client, mock_ssh):
        """Test getting category by name"""
        import json
        category = {"term_id": "2", "name": "News", "slug": "news", "parent": "0"}
        mock_ssh.execute.return_value = (json.dumps(category), "")
        
        result = wp_client.get_category_by_name("news")
        
        assert result == category
        call_args = mock_ssh.execute.call_args[0][0]
        assert "term get category 'news'" in call_args
    
    def test_get_category_by_id(self, wp_client, mock_ssh):
        """Test getting category by ID"""
        import json
        category = {"term_id": "2", "name": "News", "slug": "news", "parent": "0"}
        mock_ssh.execute.return_value = (json.dumps(category), "")
        
        result = wp_client.get_category_by_id(2)
        
        assert result == category
        call_args = mock_ssh.execute.call_args[0][0]
        assert "term get category 2" in call_args
