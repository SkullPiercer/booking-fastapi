from fastapi import status, HTTPException

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.mappers.base import DataMapper


class CRUDBase:
    model = None
    mapper: DataMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_one_by_filter(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)

        obj = result.scalars().all()
        
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Объект {self.model} не найден'
            )

        if len(obj) > 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Фидьтр вернул более одного объекта'
            )

        return self.mapper.map_to_domain_entity(obj[0])

    async def get_list(self, *filter, **filters):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filters)
        )
        result = await self.session.execute(query)
        return [
                self.mapper.map_to_domain_entity(obj)
                for obj in result.scalars().all() 
            ]
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def create(self, obj):
        query = insert(self.model).values(**obj.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        return self.mapper.map_to_domain_entity(result.scalars().one())

    async def create_bulk(self, obj):
        query = insert(self.model).values([schema.model_dump() for schema in obj])
        await self.session.execute(query)
    
    async def delete(self, **filter_by):
        query = delete(self.model).filter_by(**filter_by).returning(self.model)
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
                f'{self.model.__name__} с id={filter_by} не найден'
            )

        return self.mapper.map_to_domain_entity(deleted_obj[0])

    async def update(self, new_data, partially: bool = False, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**new_data.model_dump(exclude_unset=partially))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        updated_obj = result.scalars().one_or_none()

        if updated_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{self.model.__name__} с id={filter_by} не найден'
            )

        return self.mapper.map_to_domain_entity(updated_obj)