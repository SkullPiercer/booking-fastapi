from fastapi import status

async def test_add_booking(user_client, room):
    response = await user_client.post(
        '/bookings/',
        json={
            'room_id': room.id,
            'date_from': '2021-07-01',
            'date_to': '2021-08-01',
        }
    )

    assert response.status_code == status.HTTP_200_OK