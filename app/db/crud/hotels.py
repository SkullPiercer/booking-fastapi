from sqlalchemy import select

from app.db.crud.base import CRUDBase
from app.db.models.hotels import Hotels

class CRUDHotels(CRUDBase):
    model = Hotels

    async def get_list(
            self,
            location,
            title,
            limit,
            offset
        ):
            query = select(self.model)

            if location:
                query = query.where(Hotels.location.ilike(location))
            
            if title:
                query = query.where(Hotels.title.ilike(title))

            query = (
                query
                .limit(limit)
                .offset(offset)
            )
            
            res = await self.session.execute(query)
            return res.scalars().all()