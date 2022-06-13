from app.util import db


async def fetch_last_event_id() -> int:
    result = await db.fetch_all(
        "SELECT value FROM object_store WHERE key = ?",
        ("event.last_id",),
    )
    try:
        return int(result[0])
    except Exception:
        return 0
