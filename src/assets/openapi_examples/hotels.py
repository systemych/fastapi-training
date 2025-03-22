POST_OPENAPI_EXAMPLE = {
    "1": {"summary": "Новый объект", "value": {"title": "Владивосток 2000", "location": "Владивосток, ул.Советская, д.20"}},
    "2": {"summary": "С существующим title", "value": {"title": "Горящие вершины", "location": "Сочи, ул.Ленина, д.20"}},
    "3": {"summary": "Не валидный запрос", "value": {"title": "Каменные джунгли"}},
}

PUT_OPENAPI_EXAMPLE = {
    "1": {"summary": "Валидный запрос", "value": {"title": "Горящие вершины", "location": "Сочи, ул.Советская, д.20"}},
    "2": {"summary": "Не валидный запрос", "value": {"title": "Горящие вершины"}},
}

PATCH_OPENAPI_EXAMPLE = {
    "1": {"summary": "Все поля", "value": {"title": "Курорт в Сочи", "location": "Сочи, ул.Советская, д.20"}},
    "2": {"summary": "Часть полей", "value": {"location": "Сочи, ул.Че, д.20"}},
    "3": {"summary": "Невалидный запрос", "value": {}},
}
