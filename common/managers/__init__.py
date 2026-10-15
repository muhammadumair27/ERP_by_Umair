"""Model managers shared across applications."""

from .all_objects_manager import AllObjectsManager
from .soft_delete_manager import SoftDeleteManager

__all__ = ("AllObjectsManager", "SoftDeleteManager")
