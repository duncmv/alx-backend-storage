#!/usr/bin/env python3
"""Using Redis as a cache"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called"""

    @wraps(method)
    def wrapper(self: object, *args, **kwargs) -> Any:
        """Wrapper that increments the number of times a method is called"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs and outputs"""

    @wraps(method)
    def wrapper(self: object, *args, **kwargs) -> Any:
        """Wrapper that stores the history of inputs and outputs"""
        self._redis.rpush(method.__qualname__ + ":inputs",
                          str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs",
                          output)
        return output

    return wrapper


class Cache:
    """Cache class implemented using redis"""

    def __init__(self: object) -> None:
        """Initialize class with redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
