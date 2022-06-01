from datetime import datetime
from typing import Dict

from box import Box
from pydantic import BaseModel, AnyUrl
# from pydantic.json import Dict

from app.util.data import boxify


def boxify_http_model(model: BaseModel) -> Box:
    return boxify(model.dict(exclude_unset=True))


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


