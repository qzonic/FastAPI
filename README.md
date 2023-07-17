# Стек
<img src="https://img.shields.io/badge/Python-4169E1?style=for-the-badge"/> <img src="https://img.shields.io/badge/FastAPI-419284?style=for-the-badge"/> <img src="https://img.shields.io/badge/Docker-00BFFF?style=for-the-badge"/> <img src="https://img.shields.io/badge/PostgreSQL-87CEEB?style=for-the-badge"/> <img src="https://img.shields.io/badge/TourtoiseORM-4350af?style=for-the-badge"/>

# Описание проекта:

**Проект Cargo**

Проект Cargo опзволяет загружать данные в виде json файла, 
в котором указан тип груза, ставку за конкретный месяц и год (вне зависимости от того какой день указан в дате,
все дни приводятся к первому дню месяца, например, дата в json-файле -`2023-07-17` будет записана в БД как `2023-07-01`). Ставка за каждый месяц может изменяться.

Так же проект позволяет получить стоимость страхования груза 
в зависимости от года и месяца (например, если в запросе будет `2020-06-15`, 
то на сервере будет искаться дата `2020-06-01`, то есть номер дня из запроса приводится к первому дню месяца), объявленной стоимости и типа груза.

# Описание реализации:

В проекте используется:
* в качестве веб-фреймворка - **FastAPI**; 
* в качестве базы данных - **PostgreSQL**; 
* в качестве ORM - **Tortoise**; 
* для миграций моделий из Tortoise в БД - **Aerich**; 


# Как запустить проект:

*Клонировать репозиторий и перейти в него в командной строке:*
```
https://github.com/qzonic/FastAPI.git
```
```
cd FastAPI/
```

В директории FastAPI нужно создать .env файл, в котором указывается следующее:
```
DB_NAME=
DB_USER=
DB_PASS=
DB_HOST=db # это оставляем
DB_PORT=5432 # это оставляем

DB_NAME_TEST=
DB_USER_TEST=
DB_PASS_TEST=
DB_HOST_TEST=test_db # это оставляем
DB_PORT_TEST=5432 # это оставляем
```

*Теперь необходимо собрать Docker-контейнеры:*
```
docker-compose up -d
```

*После сборки контейнеров, нужно прописать следующие команды по очереди:*
```
docker-compose exec web aerich init -t src.settings.DATABASE_CONFIG
```

```
docker-compose exec web aerich init-db
```

*Теперь проект доступен по адресу:*
```
http://127.0.0.1:8000/
```

*Примеры взаимодействия с API:*

1. Загрузка json-файла для заполнения БД.
Файл должен иметь следующую структуру:
```json
{
  "2020-06-01": [
    {
      "cargo_type": "Glass",
      "rate": "0.04"
    },
    {
      "cargo_type": "Other",
      "rate": "0.01"
    }
  ],
  "2020-07-01": [
    {
      "cargo_type": "Glass",
      "rate": "0.035"
    },
    {
      "cargo_type": "Other",
      "rate": "0.015"
    }
  ]
}
```
Пример запроса:
```python
import asyncio

import aiohttp

url = 'http://127.0.0.1:8000/load-cargo-rate/'
file_path = 'data.json'

async def upload_data(path):
    with open(file_path, 'rb') as file:
        async with aiohttp.ClientSession() as session:
            response = await session.post(path, data={'file': file})

asyncio.run(upload_data(url))
```
Пример ответа:
```json
[
  {
    "cargo_type": "Glass",
    "rate": 0.04, 
    "date": "2020-06-01"
  }, 
  {
    "cargo_type": "Other",
    "rate": 0.01, 
    "date": "2020-06-01"
  }, 
  {
    "cargo_type": "Glass",
    "rate": 0.035, 
    "date": "2020-07-01"
  }, 
  {
    "cargo_type": "Other", 
    "rate": 0.015, 
    "date": "2020-07-01"
  }
]
```

2. Расчет стоимости страхования, зависящей от типа груза, даты и объявленной стоимости.
Пример запроса:
```python
import asyncio

import aiohttp

params = {
    'cargo_type': 'glass',
    'current_date': '2020-06-01',
    'declared_value': 100
}

url = 'http://127.0.0.1:8000/cargo'

async def calc_price(path):
    async with aiohttp.ClientSession() as session:
        response = await session.get(path, params=params)

asyncio.run(calc_price(url))
```
Пример ответа:
```json
{
  "date": "2020-06-01", 
  "cargo_type": "Glass", 
  "rate": 0.04, 
  "declared_value": 100.0, 
  "result": 4.0
}
```

# Тесты:
В проете написаны тесты, использую библиотеки pytest и pytest-asyncio. Для запуска тестов необходимо приписать:
```
docker-compose exec web pytest
```

### Автор
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/qzonic)
