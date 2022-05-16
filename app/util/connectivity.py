import os
from functools import lru_cache
from logging import Logger

import aiosqlite
import shotgun_api3 as sg
from typing import List, Any, Dict, Union

from aiosqlite import Connection
from toolz import memoize

from app.util.logger import get_logger

Map = Dict[str, Any]
_DB = os.environ.get("DB_PATH", "data.db")


class ShotgridClient:
    client: sg.Shotgun
    log: Logger = get_logger("ShotgridClient")

    def __init__(self, client: sg.Shotgun) -> None:
        self.client = client

    def find_one(
        self,
        type_: str,
        filters: List[Union[List[Any], Dict[str, str]]],
        fields: List[str],
    ) -> Map:
        return self.client.find_one(type_, filters, fields)

    def find(
        self,
        type_: str,
        filters: List[Union[List[Any], Dict[str, str]]],
        fields: List[str],
        order: List[Dict[str, str]] = None,
        limit: int = 10_000,
    ) -> List[Map]:
        return self.client.find(
            type_,
            filters,
            fields,
            order=order,
            limit=limit,
        )

    def update(self, type_: str, entity_id: int, data: Dict[str, Any]) -> Any:
        return self.client.update(type_, entity_id, data)


@lru_cache(maxsize=128)
def shotgrid() -> ShotgridClient:
    client = sg.Shotgun(
        base_url=os.environ.get("SG_URL"),
        script_name=os.environ.get("SG_SCRIPT"),
        api_key=os.environ.get("SG_SECRET_KEY"),
        convert_datetimes_to_utc=True,
    )
    return ShotgridClient(client)


@memoize
def get_fields(type_: str) -> List[str]:
    return list(shotgrid().client.schema_field_read(type_).keys())


def connect_file_db(flag: str = "rwc") -> Connection:
    return aiosqlite.connect(f"file:{_DB}?mode={flag}", uri=True)


