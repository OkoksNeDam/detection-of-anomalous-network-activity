from exceptions.base_exception import AppException


class FileExtensionException(AppException):
    def __init__(self, message):
        super().__init__(message)