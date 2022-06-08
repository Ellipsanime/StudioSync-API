import urllib.parse
from typing import Any

import attr
from box import Box
from returns.curry import curry


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeQuery:
    identifier: int | str
    field: str | None
    value: Any | None
    sort_field: str = "version_id"
    sort_order: str = "ASC"
    skip: int = 0
    limit: int = 500

    @staticmethod
    @curry
    def unbox(identifier: int | str, data: Box) -> "VersionChangeQuery":
        return VersionChangeQuery(
            urllib.parse.unquote(identifier),
            data.filter_field.value if data.filter_field else None,
            data.filter_value or None,
            data.sort_field.value,
            data.sort_order.value,
            data.skip or 0,
            data.limit or 500,
        )


@attr.s(auto_attribs=True, frozen=True)
class SimpleFetchQuery:
    sort_field: str = "id"
    sort_order: str = "ASC"
    skip: int = 0
    limit: int = 500

    @staticmethod
    def unbox(data: Box) -> "SimpleFetchQuery":
        return SimpleFetchQuery(
            data.sort_field.value,
            data.sort_order.value,
            data.skip or 0,
            data.limit or 500,
        )

