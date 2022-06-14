from typing import Dict

from pydantic import BaseModel, AnyUrl


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
