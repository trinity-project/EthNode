import redis
from config import setting

__all__=["redis_client"]

pool= redis.ConnectionPool(host=setting.REDIS_HOST,port=setting.REDIS_PORT,decode_responses=True,password=setting.REDIS_PASSWORD)

redis_client=redis.Redis(connection_pool=pool)