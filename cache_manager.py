"""
GESTOR DE CACHE INTELIGENTE
Reduz carga no Oracle e melhora performance
"""

import time
from typing import Any, Optional, Callable, Dict
from logger_config import app_logger
import threading


class CacheEntry:
    """Entrada de cache com expiração"""

    def __init__(self, value: Any, ttl: float = 300.0):
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
        self.access_count = 0
        self.last_access = self.created_at

    def is_expired(self) -> bool:
        """Verifica se entrada expirou"""
        return (time.time() - self.created_at) > self.ttl

    def access(self) -> Any:
        """Acessa valor e atualiza estatísticas"""
        self.access_count += 1
        self.last_access = time.time()
        return self.value


class CacheManager:
    """Gestor de cache com LRU e TTL"""

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
        """Inicializa o cache"""
        self.logger = app_logger
        self.cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self.hit_count = 0
        self.miss_count = 0
        self.max_size = 1000

        self.logger.info("Cache Manager inicializado")

    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        with self._lock:
            if key in self.cache:
                entry = self.cache[key]

                if entry.is_expired():
                    del self.cache[key]
                    self.miss_count += 1
                    return None

                self.hit_count += 1
                return entry.access()

            self.miss_count += 1
            return None

    def set(self, key: str, value: Any, ttl: float = 300.0):
        """Define valor no cache"""
        with self._lock:
            if len(self.cache) >= self.max_size:
                self._evict_lru()

            self.cache[key] = CacheEntry(value, ttl)

    def _evict_lru(self):
        """Remove entrada menos usada (LRU)"""
        if not self.cache:
            return

        lru_key = min(self.cache.keys(),
                      key=lambda k: self.cache[k].last_access)
        del self.cache[lru_key]
        self.logger.debug(f"Evicted LRU cache entry: {lru_key}")

    def invalidate(self, key: str):
        """Invalida entrada específica"""
        with self._lock:
            if key in self.cache:
                del self.cache[key]

    def invalidate_pattern(self, pattern: str):
        """Invalida entradas que correspondem a padrão"""
        with self._lock:
            keys_to_delete = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.cache[key]

            if keys_to_delete:
                self.logger.debug(f"Invalidated {len(keys_to_delete)} cache entries")

    def clear(self):
        """Limpa todo o cache"""
        with self._lock:
            self.cache.clear()
            self.logger.info("Cache limpo")

    def get_stats(self) -> dict:
        """Obtém estatísticas do cache"""
        with self._lock:
            total_requests = self.hit_count + self.miss_count
            hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0

            return {
                'size': len(self.cache),
                'hits': self.hit_count,
                'misses': self.miss_count,
                'hit_rate': hit_rate,
                'total_requests': total_requests
            }


def cached(ttl: float = 300.0, key_prefix: str = ""):
    """Decorator para cachear resultados de funções"""

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            cache_mgr = CacheManager()

            cache_key = f"{key_prefix or func.__name__}_{str(args)}_{str(kwargs)}"

            # Try to get from cache
            cached_value = cache_mgr.get(cache_key)
            if cached_value is not None:
                app_logger.debug(f"Cache hit: {cache_key}")
                return cached_value

            # Not in cache, execute function
            result = func(*args, **kwargs)
            cache_mgr.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


# Instância global
cache_manager = CacheManager()
