"""Embed management commands"""
import click

from praisonaiwp.core.transport import get_transport
from praisonaiwp.core.config import Config
from praisonaiwp.core.wp_client import WPClient


@click.group()
def embed():
    """Manage WordPress embeds."""
    pass


@embed.command()
@click.argument('url')
@click.option('--width', type=int, help='Embed width')
@click.option('--height', type=int, help='Embed height')
@click.option('--server', help='Server name from config')
def generate(url, width, height, server):
    """Generate embed HTML."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    cmd = f'embed generate {url}'
    if width:
        cmd += f' --width={width}'
    if height:
        cmd += f' --height={height}'
    
    result = client.cli(cmd)
    click.echo(result)


@embed.command()
@click.argument('url')
@click.option('--server', help='Server name from config')
def discover(url, server):
    """Discover embed providers."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'embed discover {url}')
    click.echo(result)


@embed.command()
@click.option('--server', help='Server name from config')
def providers(server):
    """List embed providers."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli('embed providers')
    click.echo(result)
