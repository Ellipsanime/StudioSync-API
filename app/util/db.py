from typing import Tuple, Iterator, Generator, AsyncGenerator, Coroutine, List

import aiosqlite
from aiosqlite import Connection
from box import Box

from app.util.connectivity import _DB
from app.util.data import boxify


def connect_file_db(flag: str = "rwc") -> Connection:
    return aiosqlite.connect(f"file:{_DB}?mode={flag}", uri=True)


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
