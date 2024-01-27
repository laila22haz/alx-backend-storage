#!/usr/bin/env python3
"""Writing strings to Redis class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Incrementing values"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper funtion"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """call_history"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        input_key = method.__qualname__ + ':inputs'
        self._redis.rpush(input_key, str(args))

        resut = method(self, *args, **kwargs)

        output_key = method.__qualname__ + ':outputs'

        self._redis.rpush(output_key, str(resut))

        return resut
    return wrapper


def replay(method: Callable) -> None:
    """repaly"""
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)
    for input, output in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, input.decode("utf-8"),
                output.decode("utf-8")
                )
            )


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
