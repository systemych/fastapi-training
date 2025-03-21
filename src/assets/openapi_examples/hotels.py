POST_OPENAPI_EXAMPLE = {
    "1": {"summary": "Новый объект", "value": {"title": "Владивосток", "stars": 3}},
    "2": {"summary": "С существующим title", "value": {"title": "Сочи", "stars": 4}},
    "3": {"summary": "Не валидный запрос", "value": {"title": "Москва"}},
}

PUT_OPENAPI_EXAMPLE = {
    "1": {"summary": "Валидный запрос", "value": {"title": "Сочи", "stars": 5}},
    "2": {"summary": "Не валидный запрос", "value": {"title": "SoСочиchi"}},
}

PATCH_OPENAPI_EXAMPLE = {
    "1": {"summary": "Все поля", "value": {"title": "Курорт в Сочи", "stars": 5}},
    "2": {"summary": "Часть полей", "value": {"stars": 5}},
    "3": {"summary": "Невалидный запрос", "value": {}},
}
