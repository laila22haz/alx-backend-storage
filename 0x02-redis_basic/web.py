#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker'''
from functools import wraps
import redis
import requests
from typing import Callable
import time

_redis = redis.Redis()


def cache_with_expiry(method: Callable) -> Callable:
    '''Define a decorator that tracks and sets an expired web cache'''
    @wraps(method)
    def wrapper(url: str) -> str:
        _redis.incr("count:{}".format(url))
        cached = _redis.get("{}".format(url))
        if cached:
            return cached.decode("utf-8")
        response = method(url)
        _redis.setex("{}".format(url), 10, response)
        return response
    return wrapper


@cache_with_expiry
def get_page(url: str) -> str:
    '''Return the content of an HTTP request'''
    response = requests.get(url)
    return response.text
