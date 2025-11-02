"""
TRATAMENTO CENTRALIZADO DE ERROS
Fornece mensagens consistentes e logging de erros
"""

from typing import Optional, Callable, Any
from functools import wraps
from logger_config import app_logger
from tkinter import messagebox


class ApplicationError(Exception):
    """Classe base para erros da aplicação"""
    pass


class DatabaseError(ApplicationError):
    """Erros relacionados com base de dados"""
    pass


class ValidationError(ApplicationError):
    """Erros de validação de dados"""
    pass


class ConnectionError(ApplicationError):
    """Erros de conexão"""
    pass


class ErrorHandler:
    """Gestor centralizado de erros"""

    logger = app_logger

    ERROR_MESSAGES = {
        'db_connection': 'Erro de conexão com a base de dados. Verifique as configurações.',
        'db_query': 'Erro ao executar operação na base de dados.',
        'validation': 'Dados inválidos. Verifique os campos preenchidos.',
        'unknown': 'Ocorreu um erro inesperado. Tente novamente.',
        'timeout': 'Operação expirou. Tente novamente.',
        'permission': 'Você não tem permissão para executar esta operação.',
    }

    @staticmethod
    def handle_error(error: Exception, context: str = "operação", show_ui: bool = True) -> Optional[str]:
        """Trata erro de forma centralizada"""

        error_type = type(error).__name__
        error_msg = str(error)

        ErrorHandler.logger.error(f"Erro em {context}: [{error_type}] {error_msg}")

        # Seleciona mensagem apropriada
        if isinstance(error, DatabaseError):
            user_message = ErrorHandler.ERROR_MESSAGES['db_query']
        elif isinstance(error, ValidationError):
            user_message = ErrorHandler.ERROR_MESSAGES['validation']
        elif isinstance(error, ConnectionError):
            user_message = ErrorHandler.ERROR_MESSAGES['db_connection']
        elif "timeout" in error_msg.lower():
            user_message = ErrorHandler.ERROR_MESSAGES['timeout']
        else:
            user_message = ErrorHandler.ERROR_MESSAGES['unknown']

        if show_ui:
            messagebox.showerror("Erro", user_message)

        return user_message

    @staticmethod
    def handle_success(message: str, context: str = "operação"):
        """Registra sucesso de operação"""
        ErrorHandler.logger.info(f"Sucesso em {context}: {message}")
        messagebox.showinfo("Sucesso", message)


def safe_database_operation(func: Callable) -> Callable:
    """Decorator para operações seguras com base de dados"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.handle_error(e, context=func.__name__)
            return None

    return wrapper


def safe_ui_operation(func: Callable) -> Callable:
    """Decorator para operações seguras da UI"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.handle_error(e, context=func.__name__, show_ui=True)
            return None

    return wrapper
