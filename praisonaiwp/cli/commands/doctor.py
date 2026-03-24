"""Doctor command - Check praisonaiwp configuration and connectivity"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from praisonaiwp.core.config import Config
from praisonaiwp.core.transport import get_transport
from praisonaiwp.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


@click.command()
@click.option('--server', default=None, help='Test specific server connection')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed configuration')
def doctor(server, verbose):
    """
    Check praisonaiwp configuration and connectivity
    
    Shows:
    - Configuration file location
    - Default server and website
    - All configured servers
    - Connection test results
    
    EXAMPLES:
    
        # Check configuration and default server
        praisonaiwp doctor
        
        # Test specific server connection
        praisonaiwp doctor --server praison-ai
        
        # Show detailed configuration
        praisonaiwp doctor --verbose
    """
    
    console.print()
    console.print(Panel.fit(
        "[bold cyan]PraisonAIWP Doctor[/bold cyan]\n"
        "Configuration and connectivity check",
        border_style="cyan"
    ))
    console.print()
    
    # Configuration file location
    config_path = Path.home() / ".praisonaiwp" / "config.yaml"
    console.print(f"[bold]Configuration File:[/bold]")
    console.print(f"  📁 {config_path}")
    
    if not config_path.exists():
        console.print(f"  [red]✗ Config file not found![/red]")
        console.print(f"  [yellow]Run 'praisonaiwp init' to create configuration[/yellow]")
        return
    else:
        console.print(f"  [green]✓ Config file exists[/green]")
    
    console.print()
    
    # Load configuration
    try:
        config = Config()
    except Exception as e:
        console.print(f"[red]✗ Failed to load configuration: {e}[/red]")
        return
    
    # Default server info
    default_server_name = config.data.get('default_server', 'default')
    console.print(f"[bold]Default Server:[/bold] {default_server_name}")
    
    try:
        default_server = config.get_default_server()
        website = default_server.get('website', 'Not configured')
        transport = default_server.get('transport', 'ssh')
        console.print(f"  🌐 Website: [cyan]{website}[/cyan]")
        console.print(f"  🔌 Transport: {transport}")
        
        if transport == 'kubernetes':
            console.print(f"  📦 Namespace: {default_server.get('namespace', 'default')}")
            console.print(f"  🏷️  Pod Selector: {default_server.get('pod_selector', 'N/A')}")
        else:
            hostname = default_server.get('hostname', 'N/A')
            console.print(f"  🖥️  Hostname: {hostname}")
    except Exception as e:
        console.print(f"  [red]✗ Error loading default server: {e}[/red]")
    
    console.print()
    
    # All configured servers
    servers = config.list_servers()
    console.print(f"[bold]Configured Servers:[/bold] ({len(servers)} total)")
    
    table = Table(show_header=True, header_style="bold")
    table.add_column("Name", style="cyan")
    table.add_column("Website", style="green")
    table.add_column("Transport", style="yellow")
    table.add_column("Default", style="magenta")
    
    for srv_name in servers:
        try:
            srv = config.data.get('servers', {}).get(srv_name, {})
            is_default = "✓" if srv_name == default_server_name else ""
            transport = srv.get('transport', 'ssh')
            website = srv.get('website', 'N/A')
            table.add_row(srv_name, website, transport, is_default)
        except Exception:
            table.add_row(srv_name, "Error", "", "")
    
    console.print(table)
    console.print()
    
    # Connection test
    if server or verbose:
        test_server = server or default_server_name
        console.print(f"[bold]Testing connection to '{test_server}'...[/bold]")
        
        try:
            server_config = config.get_server(test_server)
            transport = server_config.get('transport', 'ssh')
            
            if transport == 'kubernetes':
                console.print("  [yellow]⚠ Kubernetes transport - skipping SSH test[/yellow]")
                console.print(f"  [dim]Use 'kubectl get pods -l {server_config.get('pod_selector', '')}' to verify[/dim]")
            else:
                transport = get_transport(config, server)
                transport.connect()
                # Test WP-CLI
                wp_cli = server_config.get('wp_cli', '/usr/local/bin/wp')
                wp_path = server_config.get('wp_path', '')
                allow_root = server_config.get('allow_root', False)
                root_flag = ' --allow-root' if allow_root else ''
                result = transport.execute(f"cd {wp_path} && {wp_cli}{root_flag} --info 2>/dev/null | head -1")
                
                if result and 'WP-CLI' in result:
                    console.print(f"  [green]✓ SSH connection successful[/green]")
                    console.print(f"  [green]✓ WP-CLI available: {result.strip()}[/green]")
                else:
                    console.print(f"  [green]✓ SSH connection successful[/green]")
                    console.print(f"  [yellow]⚠ WP-CLI check inconclusive[/yellow]")
                    
        except Exception as e:
            console.print(f"  [red]✗ Connection failed: {e}[/red]")
    
    console.print()
    
    # Verbose configuration details
    if verbose:
        console.print("[bold]Full Configuration:[/bold]")
        settings = config.data.get('settings', {})
        for key, value in settings.items():
            console.print(f"  {key}: {value}")
        console.print()
    
    # Tips
    console.print(Panel.fit(
        "[bold]Quick Reference:[/bold]\n"
        f"• Config: ~/.praisonaiwp/config.yaml\n"
        f"• Default site: {config.data.get('servers', {}).get(default_server_name, {}).get('website', 'N/A')}\n"
        "• List posts: praisonaiwp list --server default\n"
        "• Create post: praisonaiwp create \"Title\" --content \"HTML\"",
        title="Tips",
        border_style="dim"
    ))
