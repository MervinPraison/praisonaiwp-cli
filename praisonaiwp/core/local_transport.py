"""Local transport for PraisonAIWP

Executes WP-CLI commands directly via subprocess when running on the
same server as the WordPress installation. No SSH or kubectl needed.
"""

import os
import shutil
import subprocess
from typing import Optional, Tuple

from praisonaiwp.utils.exceptions import SSHConnectionError
from praisonaiwp.utils.logger import get_logger

logger = get_logger(__name__)


class LocalTransport:
    """Executes commands locally via subprocess.

    Provides the same interface as SSHManager and KubernetesManager
    for seamless integration with the transport factory.
    """

    def __init__(
        self,
        wp_path: Optional[str] = None,
        timeout: int = 60,
        allow_root: bool = False,
    ):
        """
        Initialize Local Transport

        Args:
            wp_path: WordPress installation path (for validation)
            timeout: Command timeout in seconds (default: 60)
            allow_root: Whether running as root (default: False, auto-detected)
        """
        self.wp_path = wp_path
        self.timeout = timeout
        self.allow_root = allow_root or (os.getuid() == 0)
        self._connected = False

        logger.debug(f"LocalTransport initialized: wp_path={wp_path}, allow_root={self.allow_root}")

    def connect(self) -> "LocalTransport":
        """
        Verify local WordPress path exists.

        Returns:
            Self for chaining

        Raises:
            SSHConnectionError: If wp_path doesn't exist locally
        """
        if self.wp_path:
            if not os.path.isdir(self.wp_path):
                raise SSHConnectionError(
                    f"WordPress path not found locally: {self.wp_path}"
                )

        self._connected = True
        logger.info(f"Local transport ready (wp_path={self.wp_path})")
        return self

    def execute(self, command: str) -> Tuple[str, str]:
        """
        Execute command locally via subprocess

        Args:
            command: Shell command to execute

        Returns:
            Tuple of (stdout, stderr)

        Raises:
            SSHConnectionError: If execution fails
        """
        if not self._connected:
            self.connect()

        logger.debug(f"Executing locally: {command}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.wp_path,
            )

            stdout = result.stdout
            stderr = result.stderr

            if stderr and 'Error:' in stderr:
                if "Term doesn't exist" not in stderr:
                    logger.warning(f"Command stderr: {stderr}")

            logger.debug(f"Command completed with {len(stdout)} bytes output")
            return stdout, stderr

        except subprocess.TimeoutExpired:
            raise SSHConnectionError(f"Command timeout: {command[:100]}...")
        except Exception as e:
            raise SSHConnectionError(f"Local command execution failed: {e}")

    def upload_file(self, local_path: str, remote_path: str) -> str:
        """
        Copy a file locally (since source and destination are on same machine).

        Args:
            local_path: Source file path
            remote_path: Destination file path

        Returns:
            Destination path

        Raises:
            SSHConnectionError: If copy fails
        """
        try:
            local_path = os.path.expanduser(local_path)

            if not os.path.exists(local_path):
                raise SSHConnectionError(f"Source file not found: {local_path}")

            # Ensure destination directory exists
            os.makedirs(os.path.dirname(remote_path), exist_ok=True)

            shutil.copy2(local_path, remote_path)
            logger.info(f"Copied {local_path} to {remote_path}")
            return remote_path

        except SSHConnectionError:
            raise
        except Exception as e:
            raise SSHConnectionError(f"File copy failed: {e}")

    def close(self):
        """Close connection (no-op for local, keeps interface consistent)"""
        self._connected = False
        logger.debug("Local transport closed")

    def __enter__(self) -> "LocalTransport":
        """Context manager entry"""
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def __del__(self):
        """Cleanup on deletion"""
        try:
            self.close()
        except Exception:
            pass
