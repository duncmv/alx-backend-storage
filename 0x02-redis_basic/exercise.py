#!/usr/bin/env python3
"""Using Redis as a cache"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called"""

    @wraps(method)
    def wrapper(self: 'Cache', *args, **kwargs):
        """Wrapper that increments the number of times a method is called"""
        self._redis.incr(method.__qualname__)
        return method(*args, **kwargs)

    return wrapper


class Cache:
    """Cache class implemented using redis"""

    def __init__(self: object) -> None:
        """Initialize class with redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self: object, data: Union[str, bytes, int, float]) -> str:
        """Store data in redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self: object, key: str, fn: Callable = None) -> Union[str, bytes,
                                                                  int, float]:
        """Get data from redis"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self: object, key: str) -> str:
        """Get string from redis"""
        return self.get(key, str)

    def get_int(self: object, key: str) -> int:
        """Get int from redis"""
        return self.get(key, int)
