import sys
from datetime import datetime

from pydantic import BaseModel, Field

from app.client.record.enumeration import EnhancedVersionChangeSortableField
from app.record.enumeration import SortOrder


class PagingParams(BaseModel):
    skip: int = Field(0, title="Count of rows to be skipped")
    limit: int = Field(20_000, title="Amount of rows to return")


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
