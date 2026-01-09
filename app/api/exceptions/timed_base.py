from fastapi import HTTPException, status


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден!"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров!"


class ObjectExistsException(NabronirovalException):
    detail = "Похожий объект уже существует!"


class DateException(NabronirovalException):
    detail = "Дата выезда должна быть после даты въезда!"


class NotFoundException(NabronirovalException):
    detail = "Извините, ничего не было найдено!"


class MoreThanOneObjectException(NabronirovalException):
    detail = "Вернулось более одного объекта!"


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Комната не найдена"
