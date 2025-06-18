class DataValidationExeption(Exception):
    detail = "Start date must be less than end date"

class NotFoundExeption(Exception):
    detail = "Object not found"

class AlreadyExistsExeption(Exception):
    detail = "Item already exist"

class UnavailableExeption(Exception):
    detail: str

    def __init__(self, detail):
        self.detail = detail

class BadCredentialsExeption(Exception):
    detail = "Incorrect password"