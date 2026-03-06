"""Language management commands"""
import click

from praisonaiwp.core.transport import get_transport
from praisonaiwp.core.config import Config
from praisonaiwp.core.wp_client import WPClient


@click.group()
def language():
    """Language management."""
    pass


@language.command()
@click.option('--server', help='Server name from config')
def list(server):
    """List available languages."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli('language list')
    click.echo(result)


@language.command()
@click.argument('language_code')
@click.option('--server', help='Server name from config')
def install(language_code, server):
    """Install language."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'language install {language_code}')
    click.echo(result)


@language.command()
@click.argument('language_code')
@click.option('--server', help='Server name from config')
def activate(language_code, server):
    """Activate language."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'language activate {language_code}')
    click.echo(result)


@language.command()
@click.argument('language_code')
@click.option('--server', help='Server name from config')
def uninstall(language_code, server):
    """Uninstall language."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'language uninstall {language_code}')
    click.echo(result)


@language.command()
@click.option('--server', help='Server name from config')
def core(server):
    """Get core language."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli('language core')
    click.echo(result)
