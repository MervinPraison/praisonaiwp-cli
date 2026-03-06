"""Internationalization commands"""
import click

from praisonaiwp.core.transport import get_transport
from praisonaiwp.core.config import Config
from praisonaiwp.core.wp_client import WPClient


@click.group()
def i18n():
    """Internationalization management."""
    pass


@i18n.command()
@click.argument('domain')
@click.argument('pot_file')
@click.option('--server', help='Server name from config')
def make_pot(domain, pot_file, server):
    """Generate POT file."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'i18n make-pot {domain} {pot_file}')
    click.echo(result)


@i18n.command()
@click.argument('pot_file')
@click.argument('po_file')
@click.option('--server', help='Server name from config')
def make_mo(pot_file, po_file, server):
    """Generate MO file from PO file."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'i18n make-mo {pot_file} {po_file}')
    click.echo(result)


@i18n.command()
@click.argument('pot_file')
@click.argument('po_file')
@click.option('--server', help='Server name from config')
def update_po(pot_file, po_file, server):
    """Update PO file from POT file."""
    config = Config()
    transport = get_transport(config, server)
    transport.connect()
    client = WPClient(ssh, config.get_server(server)['wp_path'] if server else None)
    
    result = client.cli(f'i18n update-po {pot_file} {po_file}')
    click.echo(result)
