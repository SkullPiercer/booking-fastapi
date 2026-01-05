import aiofiles
import aiofiles.os
from pathlib import Path
from typing import Annotated

from fastapi import Depends, Query, UploadFile, File
from pydantic import BaseModel


class Pagination(BaseModel):
    page: Annotated[int, Query(1, description="Отелей на транице")]
    per_page: Annotated[int, Query(3, description="Страница")]


async def get_image(file: UploadFile = File(...)):
    if file is None:
        return None

    async with aiofiles.open(
        f"app/static/images/{file.filename}", "wb"
    ) as out_file:
        content = await file.read()
        await out_file.write(content)

    return file.filename


async def delete_image(filename: str) -> bool:
    file_path = Path(f"app/static/images/{filename}")

    if not file_path.exists():
        return False

    await aiofiles.os.remove(file_path)
    return True


PaginationDep = Annotated[Pagination, Depends()]
DownloadFileDep = Annotated[UploadFile, Depends(get_image)]
