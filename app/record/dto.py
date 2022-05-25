from typing import Type, Dict, Any

import attr
from box import Box
from returns.curry import curry


@curry
def dto_from_attr(ctor: Type, data: Any) -> Type:
    return ctor(**attr.asdict(data))


@attr.s(auto_attribs=True, frozen=True)
class ClientIngestSource:
    name: str
    uri: str
    meta: Dict | None
