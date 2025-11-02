"""
MONITOR DE PERFORMANCE
Rastreia performance e otimiza operações
"""

import time
from typing import Optional, Callable
from functools import wraps
from logger_config import app_logger


class PerformanceMonitor:
    """Monitor de performance centralizado"""

    def __init__(self):
        self.logger = app_logger
        self.metrics = {}
        self.slow_operations = []

    def measure_operation(self, operation_name: str, max_duration: float = 5.0):
        """Decorator para medir duração de operações"""

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time

                    # Registra métrica
                    if operation_name not in self.metrics:
                        self.metrics[operation_name] = []

                    self.metrics[operation_name].append(duration)

                    # Aviso se lento
                    if duration > max_duration:
                        self.logger.warning(
                            f"Operação lenta detectada: {operation_name} levou {duration:.2f}s"
                        )
                        self.slow_operations.append({
                            'operation': operation_name,
                            'duration': duration,
                            'timestamp': time.time()
                        })
                    else:
                        self.logger.debug(f"{operation_name} levou {duration:.3f}s")

            return wrapper

        return decorator

    def get_stats(self, operation_name: str) -> Optional[dict]:
        """Obtém estatísticas de uma operação"""
        if operation_name not in self.metrics:
            return None

        times = self.metrics[operation_name]
        return {
            'count': len(times),
            'avg': sum(times) / len(times),
            'min': min(times),
            'max': max(times),
            'last': times[-1]
        }

    def report(self):
        """Gera relatório de performance"""
        self.logger.info("=== RELATÓRIO DE PERFORMANCE ===")
        for operation_name, times in self.metrics.items():
            stats = self.get_stats(operation_name)
            self.logger.info(
                f"{operation_name}: "
                f"Execuções={stats['count']}, "
                f"Média={stats['avg']:.3f}s, "
                f"Min={stats['min']:.3f}s, "
                f"Max={stats['max']:.3f}s"
            )

        if self.slow_operations:
            self.logger.warning(f"Operações lentas detectadas: {len(self.slow_operations)}")


# Instância global
perf_monitor = PerformanceMonitor()
