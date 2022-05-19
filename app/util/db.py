from typing import Tuple, List

import aiosqlite
from aiosqlite import Connection, Cursor
from box import Box

from app.util.connectivity import _DB
from app.util.data import boxify


async def connect_file_db(flag: str = "rwc") -> Connection:
    db = await aiosqlite.connect(f"file:{_DB}?mode={flag}", uri=True)
    cursor = await db.execute("PRAGMA foreign_keys = 1;")
    await cursor.close()
    return db


async def fetch_one(
    query: str,
    params: Tuple | None = None,
) -> Box:

    db = await connect_file_db()
    cursor = await db.execute(query, params)
    row = await cursor.fetchone()
    result = boxify(dict(zip(row.keys(), row)))

    await cursor.close()
    await db.close()

    return result


async def fetch_all(
    query: str,
    params: Tuple | None = None,
) -> List[Box]:

    db = await connect_file_db()
    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    result = [boxify(dict(zip(x.keys(), x))) for x in rows]

    await cursor.close()
    await db.close()

    return result
