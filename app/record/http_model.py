from datetime import datetime
from typing import Dict

from box import Box
from pydantic import BaseModel, AnyUrl, Field
# from pydantic.json import Dict

from app.util.data import boxify


def boxify_http_model(model: BaseModel) -> Box:
    return boxify(model.dict(exclude_unset=True))


class SearchableQueryParams(BaseModel):
    filter_field: str | None = Field(title="Filter field name")
    filter_value: str | None = Field(title="Filter value")
    sort_field: str | None = Field(title="Sort-by field value")
    sort_order: int | None = Field(title="Sort-by order (1/-1)")
    skip: int | None = Field(title="Count of rows to be skipped")
    limit: int | None = Field(title="Amount of rows to return(max: 25)")


class IngestSourceHttpModel(BaseModel):
    name: str
    uri: AnyUrl
    meta: Dict | None


class ClientProjectHttpModel(BaseModel):
    id: int | None
    origin_id: int
    source: str
    name: str
    code: str | None


class ProviderProjectHttpModel(BaseModel):
    id: int | None
    origin_id: int
    name: str
    code: str | None


class VersionChangeHttpModel(BaseModel):
    id: int | None
    origin_id: int
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    processed: bool = False


class UpdateVersionChangeHttpModel(BaseModel):
    processed: bool


class FileHttpModel(BaseModel):
    id: int | None
    origin_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str


