from fastapi import status

async def test_get_facilities(async_client):
    response = await async_client.get(url='/facilities/')
    assert response.status_code == status.HTTP_200_OK


async def test_create_facility(async_client):
    response = await async_client.post(
        url='/facilities/',
        json={'title': 'Новый крутой массажёр'}
    )
    assert response.status_code == status.HTTP_200_OK