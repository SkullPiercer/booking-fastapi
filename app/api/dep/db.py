from typing import Annotated

from fastapi import Depends

from app.db.crud import CRUDHotels, CRUDUser, CRUDRooms, CRUDBookings, CRUDFacility, CRUDRoomFacility
from app.core.db import async_session_maker


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = CRUDHotels(self.session)
        self.users = CRUDUser(self.session)
        self.rooms = CRUDRooms(self.session)
        self.bookings = CRUDBookings(self.session)
        self.facility = CRUDFacility(self.session)
        self.rooms_facilities = CRUDRoomFacility(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()


async def get_db():
    async with DBManager(async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
