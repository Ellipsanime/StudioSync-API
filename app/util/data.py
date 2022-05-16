from typing import Dict, Any

from box import Box


def boxify(data: Dict[str, Any]) -> Box:
    return Box(data, frozen_box=True, default_box=True, box_dots=True)
