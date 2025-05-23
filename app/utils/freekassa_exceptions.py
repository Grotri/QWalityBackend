class FreekassaError(Exception):
    """Базовый класс для ошибок FreeKassa API"""
    def __init__(self, message, code=None, details=None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        error_msg = self.message
        if self.code:
            error_msg += f" (код ошибки: {self.code})"
        return error_msg


class FreekassaAuthError(FreekassaError):
    """Ошибка авторизации в API FreeKassa"""
    pass


class FreekassaApiError(FreekassaError):
    """Ошибка при выполнении запроса к API FreeKassa"""
    pass


class FreekassaWebhookError(FreekassaError):
    """Ошибка при обработке webhook от FreeKassa"""
    pass


class FreekassaValidationError(FreekassaError):
    """Ошибка валидации параметров запроса к API FreeKassa"""
    pass 