from .bonsai import Bonsai
from extentions.redis_client import RedisClient
from extentions.redisjson_utility import RedisJsonUtilities


# def initialize_bonsai():
#     client = RedisClient().get_instance()
#     redisjson_utility_object = RedisJsonUtilities(client)
#     rules  = redisjson_utility_object.get_values_by_key('rules')
#     rule_evaluator = Bonsai({'rules': rules})
#     return rule_evaluator

# bonsai_object = initialize_bonsai()
