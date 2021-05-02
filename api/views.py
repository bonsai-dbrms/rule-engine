from django.shortcuts import render

# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from extentions.redis_client import RedisClient
from extentions.redisjson_utility import RedisJsonUtilities
# from bonsaicore.bonsai import Bonsai

from bonsaicore import bonsai_object


class Rules(APIView):
    """
    Used for creating and retrieving rules.
    """
    def get(self, request, format=None):
        client = RedisClient().get_instance()
        redisjson_utility_object = RedisJsonUtilities(client)
        rules  = redisjson_utility_object.get_values_by_key('rules')

        return Response(rules)

    def post(self, request, format=None):
        data = request.data
        client = RedisClient().get_instance()
        redisjson_utility_object = RedisJsonUtilities(client)
        redis_response  = redisjson_utility_object.append_rules_in_redis('rules' , data)
        if redis_response:
            return Response("success", status=status.HTTP_201_CREATED)
        return Response("failiure", status=status.HTTP_400_BAD_REQUEST)

class RulesEvaluation(APIView):
    """
    Used for evaluating rules for given input 
    """
    def post(self, request, format=None):
        result = bonsai_object.process(request.data)
        return Response(result)
