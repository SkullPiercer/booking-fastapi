import pytest
from fastapi import status

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", status.HTTP_200_OK),
        (1, "2024-08-02", "2024-08-11", status.HTTP_200_OK),
        (1, "2024-08-03", "2024-08-12", status.HTTP_200_OK),
        (2, "2024-08-17", "2024-08-25", status.HTTP_200_OK),
        (1, "2024-08-06", "2024-08-15", status.HTTP_400_BAD_REQUEST),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, user_client
):
    response = await user_client.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": "2021-07-01",
            "date_to": "2021-08-01",
        },
    )
    assert response.status_code == status_code


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-02", "2024-08-11", 2),
        (1, "2024-08-03", "2024-08-12", 3),
    ],
)
async def test_add_and_get_my_bookings(
    delete_all_bookings, user_client, room_id, date_from, date_to, booked_rooms
):
    response = await user_client.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": "2021-07-01",
            "date_to": "2021-08-01",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    resp_user_book = await user_client.get("/bookings/me")
    assert resp_user_book.status_code == status.HTTP_200_OK
    assert len(resp_user_book.json()) == booked_rooms
