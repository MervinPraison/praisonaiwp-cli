"""Transport factory for PraisonAIWP

Provides unified transport creation based on server configuration.
Supports SSH (default), Kubernetes, and Local transports.
"""

import os
import socket
from typing import Optional, Union

from praisonaiwp.utils.logger import get_logger

logger = get_logger(__name__)


def _is_local(server_config: dict) -> bool:
    """Auto-detect if the server is the local machine.

    Returns True when:
      - hostname is missing / empty
      - hostname is localhost or 127.0.0.1
      - hostname matches the machine's own hostname
      - wp_path exists on the local filesystem AND no hostname is set
    """
    hostname = server_config.get("hostname", "").strip()

    # No hostname → local
    if not hostname:
        return True

    # Explicit localhost
    if hostname in ("localhost", "127.0.0.1", "::1"):
        return True

    # Matches machine hostname
    try:
        if hostname == socket.gethostname():
            return True
        if hostname == socket.getfqdn():
            return True
    except Exception:
        pass

    # wp_path exists locally and hostname looks like localhost
    wp_path = server_config.get("wp_path", "")
    if wp_path and os.path.isdir(wp_path) and not hostname:
        return True

    return False


def get_transport(config, server_name: Optional[str] = None):
    """
    Factory function to create the appropriate transport manager
    based on server configuration.

    Args:
        config: Config instance
        server_name: Server name from config (optional, uses default if not provided)

    Returns:
        SSHManager, KubernetesManager, or LocalTransport instance

    Transport selection:
        - ``transport: kubernetes`` or ``transport: k8s`` → KubernetesManager
        - ``transport: local`` → LocalTransport
        - ``transport: ssh`` (default) → SSHManager, unless auto-detected as local
    """
    server_config = config.get_server(server_name)
    transport_type = server_config.get("transport", "ssh").lower()

    # --- Kubernetes ---
    if transport_type in ("kubernetes", "k8s"):
        from praisonaiwp.core.kubernetes_manager import KubernetesManager

        logger.info(f"Using Kubernetes transport for server: {server_name or 'default'}")
        return KubernetesManager(
            pod_name=server_config.get("pod_name"),
            pod_selector=server_config.get("pod_selector"),
            namespace=server_config.get("namespace", "default"),
            container=server_config.get("container"),
            context=server_config.get("context"),
            timeout=server_config.get("timeout", 30),
        )

    # --- Local (explicit or auto-detected) ---
    if transport_type == "local" or (transport_type == "ssh" and _is_local(server_config)):
        from praisonaiwp.core.local_transport import LocalTransport

        logger.info(f"Using local transport for server: {server_name or 'default'}")
        return LocalTransport(
            wp_path=server_config.get("wp_path"),
            timeout=server_config.get("timeout", 60),
            allow_root=server_config.get("allow_root", False),
        )

    # --- SSH (default) ---
    from praisonaiwp.core.ssh_manager import SSHManager

    logger.debug(f"Using SSH transport for server: {server_name or 'default'}")
    return SSHManager(
        hostname=server_config.get("hostname"),
        username=server_config.get("username"),
        key_file=server_config.get("key_filename") or server_config.get("key_file"),
        port=server_config.get("port", 22),
        timeout=server_config.get("timeout", 30),
    )


# Type alias for transport managers
TransportManager = Union["SSHManager", "KubernetesManager", "LocalTransport"]

