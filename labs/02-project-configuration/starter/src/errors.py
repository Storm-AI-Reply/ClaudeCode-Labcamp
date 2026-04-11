class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: int | str):
        super().__init__(f"{resource} {resource_id} not found", status_code=404)
