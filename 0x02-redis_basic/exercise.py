#!/usr/bin/env python3
"""Writing strings to Redis class"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """Incrementing values"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper funtion"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    def __init__(self):
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis using a random key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[None, str, bytes, int, float]:
        """convert the data back to the desired format"""
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """convert the data back to the desired format"""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """convert the data back to the desired format"""
        return self.get(key, int)

