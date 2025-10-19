from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class Pagination(BaseModel):
    page: Annotated[int, Query(1, description='Отелей на транице')]
    per_page: Annotated[int, Query(3, description='Страница')]


PaginationDep = Annotated[Pagination, Depends()]
