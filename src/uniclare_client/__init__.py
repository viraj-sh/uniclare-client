from importlib.metadata import PackageNotFoundError, version

from uniclare_client.core.errors import AppError

try:
    __version__ = version("uniclare-client")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = ["AppError", "__version__"]
