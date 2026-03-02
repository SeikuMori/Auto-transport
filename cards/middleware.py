import threading

# Thread-local storage для сохранения информации о текущем пользователе
_thread_locals = threading.local()


def get_current_user():
    """Получить текущего пользователя из thread-local storage"""
    return getattr(_thread_locals, 'user', None)


def get_current_ip():
    """Получить IP текущего пользователя из thread-local storage"""
    return getattr(_thread_locals, 'ip', None)


class AuditMiddleware:
    """
    Middleware для сохранения информации о текущем пользователе и IP адресе.
    Информация сохраняется в thread-local переменных для доступа из signals.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Сохраняем пользователя и IP в thread-local storage
        _thread_locals.user = request.user
        _thread_locals.ip = self._get_client_ip(request)

        # Также сохраняем в объект запроса для прямого доступа
        request.audit_user = request.user
        request.audit_ip = _thread_locals.ip

        response = self.get_response(request)
        return response

    @staticmethod
    def _get_client_ip(request):
        """Получить IP адрес клиента из различных источников"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
