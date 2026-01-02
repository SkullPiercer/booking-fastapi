import json

import aiofiles


async def read_file(file_name, mode='r'):
    async with aiofiles.open(
            file_name,
            mode=mode,
            encoding='utf-8'
    ) as f:
        content = await f.read()
        return json.loads(content)