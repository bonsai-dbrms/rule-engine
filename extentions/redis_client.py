from django.conf import settings
from rejson import Client

from redistimeseries.client import Client as TSDBClient


class RedisClient:
    SINGLETON_INSTANCE = None

    def get_instance(self):
        if not RedisClient.SINGLETON_INSTANCE:
            RedisClient.SINGLETON_INSTANCE = Client(host='redis-12112.c245.us-east-1-3.ec2.cloud.redislabs.com',
                                                    port=12112, decode_responses=True,
                                                    password='HnQfZnVJtOjP7Tw7bLQgFuC9YW3RJeHK')

        return RedisClient.SINGLETON_INSTANCE


class RedisTSClient:
    SINGLETON_INSTANCE = None

    def get_instance(self):
        if not RedisTSClient.SINGLETON_INSTANCE:
            RedisTSClient.SINGLETON_INSTANCE = TSDBClient(host='redis-19934.c257.us-east-1-3.ec2.cloud.redislabs.com',
                                                    port=19934, decode_responses=True,
                                                    password='oFtj94WehNxi2ellRF41p59gylrlF33q')

        return RedisTSClient.SINGLETON_INSTANCE
