from fastapi import status


async def test_get_hotels(async_client):
    response = await async_client.get(
        url="hotels/",
        params={
            "date_from": "2021-07-01",
            "date_to": "2021-07-02",
        },
    )
    assert response.status_code == status.HTTP_200_OK
