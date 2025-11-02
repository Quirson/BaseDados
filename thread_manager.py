"""
GESTOR DE THREADS COM SINCRONIZAÇÃO E POOL
Garante operações thread-safe e evita race conditions
"""

import threading
from queue import Queue, Empty
from typing import Callable, Any, Optional
from concurrent.futures import ThreadPoolExecutor, Future
from logger_config import app_logger
import time


class ThreadSafeQueue:
    """Fila thread-safe para comunicação entre threads"""

    def __init__(self, maxsize: int = 0):
        self.queue = Queue(maxsize=maxsize)
        self.logger = app_logger

    def put(self, item: Any, timeout: float = 5.0):
        """Adiciona item à fila de forma segura"""
        try:
            self.queue.put(item, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Erro ao adicionar à fila: {str(e)}")

    def get(self, timeout: float = 5.0) -> Optional[Any]:
        """Obtém item da fila de forma segura"""
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None
        except Exception as e:
            self.logger.error(f"Erro ao obter da fila: {str(e)}")
            return None


class DatabaseOperationThread(threading.Thread):
    """Thread segura para operações de banco de dados"""

    def __init__(self, db_connection, query: str, params: dict = None, callback: Callable = None):
        super().__init__(daemon=True)
        self.db_connection = db_connection
        self.query = query
        self.params = params
        self.callback = callback
        self.logger = app_logger
        self.result = None
        self.error = None

    def run(self):
        """Executa operação de banco de dados"""
        try:
            self.logger.debug(f"Iniciando thread para query: {self.query[:50]}...")

            self.result = self.db_connection.execute_query(
                self.query,
                self.params,
                fetch=True
            )

            if self.callback:
                self.callback(self.result, None)

        except Exception as e:
            self.logger.error(f"Erro na thread de banco de dados: {str(e)}")
            self.error = e
            if self.callback:
                self.callback(None, e)


class ThreadPool:
    """Pool de threads gerenciado para operações assincronas"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa o pool"""
        self.logger = app_logger
        self.executor = ThreadPoolExecutor(
            max_workers=4,  # Limited to 4 threads to prevent resource exhaustion
            thread_name_prefix="Inc_DB_"
        )
        self.active_tasks = {}
        self._lock = threading.Lock()

    def submit_task(self, func: Callable, *args, **kwargs) -> Optional[str]:
        """Submete uma tarefa para execução"""
        try:
            task_id = f"task_{int(time.time() * 1000)}"

            future = self.executor.submit(self._run_with_error_handling, func, *args, **kwargs)

            with self._lock:
                self.active_tasks[task_id] = {
                    'future': future,
                    'start_time': time.time(),
                    'func_name': func.__name__
                }

            self.logger.debug(f"Tarefa submetida: {task_id}")
            return task_id

        except Exception as e:
            self.logger.error(f"Erro ao submeter tarefa: {str(e)}")
            return None

    @staticmethod
    def _run_with_error_handling(func: Callable, *args, **kwargs) -> Any:
        """Executa função com tratamento de erro"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            app_logger.error(f"Erro na execução de thread: {str(e)}")
            raise

    def get_result(self, task_id: str, timeout: float = 30.0) -> Optional[Any]:
        """Obtém resultado de uma tarefa"""
        with self._lock:
            if task_id not in self.active_tasks:
                return None

            task = self.active_tasks[task_id]
            future = task['future']

        try:
            result = future.result(timeout=timeout)

            with self._lock:
                del self.active_tasks[task_id]

            return result

        except Exception as e:
            self.logger.error(f"Erro ao obter resultado da tarefa {task_id}: {str(e)}")
            return None

    def shutdown(self):
        """Encerra o pool de forma segura"""
        self.logger.info("Encerrando pool de threads...")
        self.executor.shutdown(wait=True)
        self.logger.info("Pool de threads encerrado")


class BackgroundTask:
    """Classe para gerenciar tarefas em background"""

    def __init__(self, func: Callable, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.logger = app_logger
        self.thread = None
        self.result = None
        self.error = None
        self.is_running = False

    def start(self):
        """Inicia a tarefa em background"""
        if self.is_running:
            self.logger.warning("Tarefa já está em execução")
            return

        self.is_running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        """Executa a tarefa"""
        try:
            self.logger.debug(f"Iniciando tarefa: {self.func.__name__}")
            self.result = self.func(*self.args, **self.kwargs)
            self.logger.debug(f"Tarefa concluída: {self.func.__name__}")
        except Exception as e:
            self.logger.error(f"Erro na tarefa: {str(e)}")
            self.error = e
        finally:
            self.is_running = False

    def wait(self, timeout: float = 30.0) -> bool:
        """Aguarda conclusão da tarefa"""
        if self.thread:
            self.thread.join(timeout=timeout)
            return not self.is_running
        return False

    def get_result(self) -> Optional[Any]:
        """Obtém resultado da tarefa"""
        if self.error:
            raise self.error
        return self.result


# Instância global
thread_pool = ThreadPool()
