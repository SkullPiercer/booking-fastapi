# booking-fastapi

Простой сервис для бронирования отелей.

## Стек технологий

- Python
- FastAPI
- Uvicorn
- Pydantic

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/booking-fastapi.git
   cd booking-fastapi
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   # Для Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Для macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск

Для запуска приложения выполните команду:

```bash
uvicorn main:app --reload
```

Сервис будет доступен по адресу http://127.0.0.1:8000.

## Автор

Денисов Александр