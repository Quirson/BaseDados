"""
CONFIGURAÇÃO AVANÇADA DE LOGGING
Fornece logging estruturado e tratamento de erros
"""

import logging
import traceback
from functools import wraps
from datetime import datetime


class AppLogger:
    """Logger centralizado para toda a aplicação"""

    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa o logger"""
        import os
        os.makedirs('logs', exist_ok=True)

        self._logger = logging.getLogger('INC_Publicidade')
        self._logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def get_logger(self):
        return self._logger


def log_execution(func):
    """Decorator para logar execução de funções"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = AppLogger().get_logger()
        logger.debug(f"Iniciando: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Sucesso: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Erro em {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    return wrapper


def safe_operation(default_return=None):
    """Decorator para operações seguras com tratamento de erro"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = AppLogger().get_logger()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Erro em {func.__name__}: {str(e)}")
                logger.error(traceback.format_exc())
                return default_return

        return wrapper

    return decorator


# Instância global
app_logger = AppLogger().get_logger()
