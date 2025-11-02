import time
from typing import Any, Dict, Tuple, Optional

class Cache:
    def __init__(self, default_ttl: int = 60):
        self.store: Dict[str, Tuple[float, Any]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str):
        rec = self.store.get(key)
        if not rec:
            return None
        expires, value = rec
        if time.time() > expires:
            self.store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        ttl = ttl if ttl is not None else self.default_ttl
        self.store[key] = (time.time() + ttl, value)
