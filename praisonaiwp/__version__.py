from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("praisonaiwp")
except PackageNotFoundError:
    __version__ = "unknown"
