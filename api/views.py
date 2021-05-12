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

from bonsaicore import initialize_bonsai , EvaluationInput

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
        rule  = redisjson_utility_object.get_values_by_key('all_rules','.' + str(namespace)+'.' + str(rule_id))

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
        redis_response  = redisjson_utility_object.append_rules_in_redis('all_rules' ,'.'+str(namespace) + '.' + str(rule_id), data , namespace)
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
        rules  = redisjson_utility_object.get_values_by_key('all_rules','.' + str(namespace)).values()
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
        #format of rule data in redis
        """
        "tax_system"{
        "a1": {
            "id": a1,
            "namespace": "tax_system",
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
        },
        "a2": {
            "id": a2,
            "namespace": "tax_system",
            "rule_description": "this is a test rule 2",
            "predicates": [
            {
                "attribute_name": "Province",
                "operator": "eq",
                "type": "string",
                "value": "British Columbia"
            },
            {
                "attribute_name": "City",
                "operator": "eq",
                "type": "string",
                "value": "Vancouver"
            }
            ],
            "result": ,
            {
            "attribute_name": "tax_rate",
            "operator": "eq",
            "type": "string",
            "value": "40"
            }
        }
        }
        """
        #nipun to edit this
        bonsai_object = initialize_bonsai()
        eval_input = EvaluationInput.build(raw_input= request.data)
        print(eval_input.__dict__)
        result = bonsai_object.process(eval_input = eval_input)


        #result should be in this format
        return Response(result.__dict__)

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
        rules  = redisjson_utility_object.get_values_by_key('all_rules','.' + str(namespace)).values()
        # print(rules)
        attributes_in_namespace = set()
        for rule in rules:
            # print(rule)
            for attributes in rule.get('predicates' , []):
                print(attributes)
                attributes_in_namespace.add(attributes.get('attribute_name') + ':' + attributes.get('type'))
        
        
        print(attributes_in_namespace)
        attributes = []
        for attribute in list(attributes_in_namespace):
            attribute_components = attribute.split(':')
            attribute_dict ={'attribute_name':attribute_components[0] , 'type': attribute_components[1]}
            attributes.append(attribute_dict)
        
        return Response({'attributes':attributes})
