from django.shortcuts import render

# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from extentions.redis_client import RedisClient
from extentions.redisjson_utility import RedisJsonUtilities
import json
# from bonsaicore.bonsai import Bonsai

# from bonsaicore import bonsai_object
"""
evaluation ke lia values get karne ke lia api
evaluation ki values submit karne ke lia api
all tasks list api
eve button par click karke uske rules ka data get karne ki

"""
# add error handling and validation in all api's
class Rule(APIView):
    """
    Used for creating and retrieving rules.
    """
    def get(self, request, format=None): 
        """
        Params: namepsapce

        example: namespace = "LoyaltySystem"
        """
        namespace = request.GET.get('namespace')
        rule_id = request.GET.get('rule_id')
        client = RedisClient().get_instance()
        redisjson_utility_object = RedisJsonUtilities(client)
        rule  = redisjson_utility_object.get_values_by_key(namespace,'.' + str(rule_id))

        return Response(rule)

    def post(self, request, format=None):
        """
        body : 
            {
            "id": 123456,
            "namespace":"tax_system",
            "rule_description": "this is a test rule",
            "predicates": [
                {
                "attribute_name": "Province",
                "operator": "eq",
                "type": "string",
                "value": "Ontario"
                },
                {
                "attribute_name": "City",
                "operator": "eq",
                "type": "string",
                "value": "Toronto"
                }
            ],
            "result": ,
            {
                "attribute_name": "tax_rate",
                "operator": "eq",
                "type": "string",
                "value": "35"
            }
            }
        """
        data = request.data
        namespace = data.get('namespace')
        rule_id  = data.get('id')
        print()
        client = RedisClient().get_instance()
        redisjson_utility_object = RedisJsonUtilities(client)
        redis_response  = redisjson_utility_object.append_rules_in_redis(namespace ,'.' + str(rule_id), data)
        if redis_response:
            return Response("success", status=status.HTTP_201_CREATED)
        return Response("failiure", status=status.HTTP_400_BAD_REQUEST)

class Rules(APIView):
    """
    Bulk rule API's
    """

    def get(self , request , format = None):
        namespace = request.GET.get('namespace')
        client = RedisClient().get_instance()
        redisjson_utility_object = RedisJsonUtilities(client)
        rules  = redisjson_utility_object.get_values_by_key(namespace,'.').values()
        return Response(rules)


class RulesEvaluation(APIView):
    """
    Used for evaluating rules for given input 
    """
    def post(self, request, format=None):
        """
        Body: 

            "namespace":"TaxSystem"
            "predicates": [
                {
                "attribute_name": "Province",
                "operator": "eq",
                "type": "string",
                "value": "Ontario"
                },
                {
                "attribute_name": "City",
                "operator": "eq",
                "type": "string",
                "value": "Toronto"
                }
            ]
        
        Response: 
        {
        "rule_execution_order":[1,2,3],
        "outputs": [
                {
                "attribute_name": "tax_rate",
                "operator": "eq",
                "type": "int",
                "value": 35
                }
            ]
        }
        """
        # result = bonsai_object.process(request.data)
        return Response({
        "rule_execution_order":[1,2,3],
        "outputs": [
                {
                "attribute_name": "tax_rate",
                "operator": "eq",
                "type": "int",
                "value": 35
                }
            ]
        })

class Attributes(APIView):
    """
    Used for evaluating rules for given input 
    example: namespace = "LoyaltySystem"

    """
    def get(self, request, format=None):
        # result = bonsai_object.process(request.data)
        namespace = request.GET.get('namespace')
        client = RedisClient().get_instance()
        redisjson_utility_object = RedisJsonUtilities(client)
        rules  = redisjson_utility_object.get_values_by_key(namespace,'.').values()
        # print(rules)
        attributes_in_namespace = set()
        for rule in rules:
            # print(rule)
            for attributes in rule.get('predicates' , []):
                print(attributes)
                attributes_in_namespace.add(attributes.get('attribute_name') + ':' + attributes.get('type'))
        
        
        print(attributes_in_namespace)

        return Response(list(attributes_in_namespace))
