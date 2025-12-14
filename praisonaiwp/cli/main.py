"""Main CLI entry point for PraisonAIWP"""

import click
from praisonaiwp.__version__ import __version__
from praisonaiwp.cli.commands.init import init_command
from praisonaiwp.cli.commands.create import create_command
from praisonaiwp.cli.commands.update import update_command
from praisonaiwp.cli.commands.find import find_command
from praisonaiwp.cli.commands.list import list_command
from praisonaiwp.cli.commands.category import category_command
from praisonaiwp.cli.commands.media import media_command
from praisonaiwp.cli.commands.install_wp_cli import install_wp_cli
from praisonaiwp.cli.commands.find_wordpress import find_wordpress

# Try to import AI commands (optional)
try:
    from praisonaiwp.cli.commands.ai_commands import ai
    AI_COMMANDS_AVAILABLE = True
except ImportError:
    AI_COMMANDS_AVAILABLE = False


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    PraisonAIWP - AI-powered WordPress content management
    
    Simple, powerful WordPress automation via WP-CLI over SSH.
    
    Examples:
    
        # Initialize configuration
        praisonaiwp init
        
        # Create a post
        praisonaiwp create "My Post" --content "Hello World"
        
        # Update specific line
        praisonaiwp update 123 "old" "new" --line 10
        
        # Find text
        praisonaiwp find "search text"
        
        # List posts
        praisonaiwp list --type page
    """
    pass


# Register commands
cli.add_command(init_command, name='init')
cli.add_command(install_wp_cli, name='install-wp-cli')
cli.add_command(find_wordpress, name='find-wordpress')
cli.add_command(create_command, name='create')
cli.add_command(update_command, name='update')
cli.add_command(find_command, name='find')
cli.add_command(list_command, name='list')
cli.add_command(category_command, name='category')
cli.add_command(media_command, name='media')

# Register AI commands if available
if AI_COMMANDS_AVAILABLE:
    cli.add_command(ai, name='ai')


if __name__ == '__main__':
    cli()
