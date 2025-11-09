hotel_examples = {
    'simple_hotel': {
        'summary': 'Обычный отель',
        'value': {'title': 'Sunrise Hotel', 'location': 'Алматы'},
    },
    'resort_hotel': {
        'summary': 'Курортный отель у моря',
        'value': {'title': 'Blue Lagoon Resort', 'location': 'Сочи'},
    },
    'business_hotel': {
        'summary': 'Отель для командировок',
        'value': {'title': 'City Inn', 'location': 'Москва'},
    },
}

hotel_responses={
        200: {
            "description": "Успешный ответ со списком отелей",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "Grand Hotel Astoria",
                            "location": "Алматы, пр. Абая 45",
                            "description": "Элегантный отель с видом на горы.",
                            "rooms_count": 120,
                            "rating": 4.7
                        },
                        {
                            "id": 2,
                            "title": "Ocean View Resort",
                            "location": "Актобе, ул. Победы 10",
                            "description": "Отель с бассейном и спа-зоной.",
                            "rooms_count": 80,
                            "rating": 4.5
                        }
                    ]
                }
            }
        }
    }