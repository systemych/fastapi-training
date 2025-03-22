POST_OPENAPI_EXAMPLE = {
    "1": {"summary": "Новый объект", "value": {"title": "Владивосток", "location": "ул.Советская, д.20"}},
    "2": {"summary": "С существующим title", "value": {"title": "Сочи", "location": "ул.Ленина, д.20"}},
    "3": {"summary": "Не валидный запрос", "value": {"title": "Москва"}},
}

PUT_OPENAPI_EXAMPLE = {
    "1": {"summary": "Валидный запрос", "value": {"title": "Сочи", "location": "ул.Советская, д.20"}},
    "2": {"summary": "Не валидный запрос", "value": {"title": "Сочи"}},
}

PATCH_OPENAPI_EXAMPLE = {
    "1": {"summary": "Все поля", "value": {"title": "Курорт в Сочи", "location": "ул.Советская, д.20"}},
    "2": {"summary": "Часть полей", "value": {"location": "ул.Советская, д.20"}},
    "3": {"summary": "Невалидный запрос", "value": {}},
}
