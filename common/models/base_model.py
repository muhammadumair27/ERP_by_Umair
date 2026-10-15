"""Composite abstract base model for ERP domain entities."""

from .soft_delete_model import SoftDeleteModel
from .time_stamped_model import TimeStampedModel
from .uuid_model import UUIDModel


class BaseModel(UUIDModel, TimeStampedModel, SoftDeleteModel):
    """UUID primary key plus audit timestamps plus reversible deletion."""

    class Meta:
        abstract = True
