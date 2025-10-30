from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class CRUDBase:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create(self, obj):
        db_obj = self.model(**obj.model_dump())
        self.session.add(db_obj)
        return db_obj
