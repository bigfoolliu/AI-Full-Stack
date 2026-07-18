import hashlib
import json
import logging
from typing import Any

import redis
from redis import Redis

from app.core.config import CACHE_ENABLED, REDIS_URL

logger = logging.getLogger(__name__)

_client: Redis | None = None


def get_client() -> Redis | None:
    global _client
    if not CACHE_ENABLED or not REDIS_URL:
        return None
    if _client is None:
        try:
            _client = Redis.from_url(REDIS_URL, decode_responses=True)
            _client.ping()
        except redis.ConnectionError:
            logger.warning("Redis 连接失败，缓存已禁用")
            _client = None
    return _client


def close():
    global _client
    if _client:
        _client.close()
        _client = None


def _hash_key(prefix: str, *parts: str | int) -> str:
    raw = ":".join(str(p) for p in parts)
    if len(raw) > 200:
        raw = f"{prefix}:{hashlib.md5(raw.encode()).hexdigest()}"
    return f"kb:{raw}"


def cache_get(key: str) -> Any | None:
    client = get_client()
    if not client:
        return None
    try:
        data = client.get(key)
        return json.loads(data) if data else None
    except redis.RedisError:
        return None


def cache_set(key: str, value: Any, ttl: int = 300):
    client = get_client()
    if not client:
        return
    try:
        client.setex(key, ttl, json.dumps(value, default=str))
    except redis.RedisError:
        pass


def cache_delete_pattern(pattern: str):
    client = get_client()
    if not client:
        return
    try:
        for key in client.scan_iter(match=pattern):
            client.delete(key)
    except redis.RedisError:
        pass
