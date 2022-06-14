from datetime import datetime
from typing import Dict

from pydantic import BaseModel, AnyUrl, Field

from app.client.record.enumeration import (
    EnhancedVersionChangeSortableField,
)
from app.record.enumeration import SortOrder
from app.record.http_model import PagingParams


class VersionChangeFetchParams(PagingParams):
    datetime_min: datetime | None = Field(
        datetime.fromtimestamp(0),
        title="Datetime min",
    )
    datetime_max: datetime | None = Field(
        datetime.fromtimestamp(32536799999-1),
        title="Datetime max",
    )
    project_name: str | None = Field(None, title="Project name")
    sort_field: EnhancedVersionChangeSortableField = Field(
        EnhancedVersionChangeSortableField.VERSION_ID,
        title="Sort-by field value",
    )
    sort_order: SortOrder = Field(SortOrder.ASC, title="Sort-by order")


class OriginParams(BaseModel):
    name: str
    uri: AnyUrl
    crawling_frequency: int
    connection_info: Dict | None


class ProjectParams(BaseModel):
    name: str
    provider_project_id: int


class UpdateVersionChangeParams(BaseModel):
    processed: bool
