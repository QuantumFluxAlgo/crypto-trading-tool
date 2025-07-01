
import os

if os.getenv("TESTING"):
    import redislite
    _redis_server = redislite.StrictRedis(port=6379)
