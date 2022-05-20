from typing import List

from box import Box

from app.util import db
from app.util.data import boxify


async def fetch_version_changes(project_id: int) -> List[Box]:
    raw_changes = await db.fetch_all(
        "SELECT * FROM client_version_file_view WHERE project_id =?",
        (project_id,),
    )
    linked_files = [
        boxify(
            {
                k.replace("file_", ""): v
                for k, v in x.items()
                if k.startswith("file_")
            }
        )
        for x in raw_changes
    ]
    version = {
        k: v for k, v in raw_changes[0] if k.startswith("version_")
    }
