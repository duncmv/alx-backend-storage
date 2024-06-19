#!/usr/bin/env python3
"""expiring web cache and tracker"""
import requests
import redis
from functools import wraps
from typing import Callable


redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Decortator for counting """
    @wraps(method)
    def wrapper(url):
        """ Wrapper for decorator """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.set(f"cached:{url}", html, ex=10)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a  URL """
    req = requests.get(url)
    return req.text
