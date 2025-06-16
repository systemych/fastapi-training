CREATE_ROOM_EXAMPLE = {
    "1": {
        "summary": "Новый объект",
        "value": {
            "hotel_id": 1,
            "title": "3 кровати",
            "description": "Номер для всей семьи",
            "price": 5000,
            "quantity": 10,
            "options_ids": [1, 2],
        },
    }
}

UPDATE_ROOM_EXAMPLE = {
    "1": {
        "summary": "Все поля",
        "value": {
            "title": "3 кровати",
            "description": "Номер для всей семьи",
            "price": 6000,
            "quantity": 5,
            "options_ids": [1, 2],
        },
    }
}

EDIT_ROOM_EXAMPLE = {
    "1": {
        "summary": "Все поля",
        "value": {
            "title": "3 кровати",
            "description": "Номер для всей семьи",
            "price": 6000,
            "quantity": 5,
            "options_ids": [1, 2],
        },
    },
    "2": {"summary": "Часть полей", "value": {"price": 6000, "quantity": 5}},
}
