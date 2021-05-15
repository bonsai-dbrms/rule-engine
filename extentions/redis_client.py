from django.conf import settings
from rejson import Client

from redistimeseries.client import Client as TSDBClient
import os

class RedisClient:
    SINGLETON_INSTANCE = None

    def get_instance(self):
        if not RedisClient.SINGLETON_INSTANCE:
            RedisClient.SINGLETON_INSTANCE = Client(host=os.environ['redis_host'],
                                                    port=os.environ['redis_port'], decode_responses=True,
                                                    password=os.environ['redis_password'])

        return RedisClient.SINGLETON_INSTANCE


class RedisTSClient:
    SINGLETON_INSTANCE = None

    def get_instance(self):
        if not RedisTSClient.SINGLETON_INSTANCE:
            RedisTSClient.SINGLETON_INSTANCE = TSDBClient(host=os.environ['redis_ts_host'],
                                                    port=os.environ['redis_ts_port'], decode_responses=True,
                                                    password=os.environ['redis_ts_password'])

        return RedisTSClient.SINGLETON_INSTANCE
