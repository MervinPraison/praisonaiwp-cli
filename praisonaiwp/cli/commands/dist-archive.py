"""Distribution archive commands"""
import click

from praisonaiwp.core.transport import get_transport
from praisonaiwp.core.config import Config
from praisonaiwp.core.wp_client import WPClient


@click.command()
@click.argument('path')
@click.option('--format', default='zip', help='Archive format (zip, tar)')
@click.option('--server', help='Server name from config')
def dist_archive(path, format, server):
    """Create distribution archive."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'dist-archive {path} --format={format}')
    click.echo(result)
