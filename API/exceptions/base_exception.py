class AppException(Exception):
    def __init__(self, message: str, *args):
        self.message = message
        super().__init__(message, *args)

    def __str__(self):
        return self.message
