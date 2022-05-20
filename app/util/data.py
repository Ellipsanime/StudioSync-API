from typing import Dict, Any

from box import Box


def boxify(data: Dict[str, Any]) -> Box:
    return Box(
        data,
        frozen_box=True,
        default_box=True,
        default_box_create_on_get=False,
        default_box_none_transform=False,
        box_dots=True,
    )


def to_record(data: Dict[str, Any]) -> Box:
    return boxify(
        {
            "id": None,
            **dict(data),
        }
    )
