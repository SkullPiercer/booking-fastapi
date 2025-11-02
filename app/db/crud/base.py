from fastapi import status, HTTPException

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

class CRUDBase:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars.one_or_none()
    
    async def create(self, obj):
        query = insert(self.model).values(**obj.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().one()
    
    async def delete(self, obj_id: int):
        query = delete(self.model).where(self.model.id == obj_id).returning(self.model)
        result = await self.session.execute(query)
        
        deleted_obj = result.scalars().all()

        if len(deleted_obj) > 1:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                'Фильтр отдает больше одного обьекта!'
            )
        
        if not deleted_obj:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'{self.model.__name__} с id={obj_id} не найден'
            )

        return deleted_obj[0]

    async def update_partially(self, obj_id, new_data):
        query = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**new_data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(query)
        updated_obj = result.scalars().one_or_none()

        if updated_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{self.model.__name__} с id={obj_id} не найден'
            )

        return updated_obj