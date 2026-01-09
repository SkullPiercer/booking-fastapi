from datetime import date
from fastapi import HTTPException, status


def check_date_to_after_date_from(date_to: date, date_from: date):
    if date_to <= date_from:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Дата заезда не может быть позже даты выезда!'
        )
