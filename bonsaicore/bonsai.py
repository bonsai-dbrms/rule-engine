import json

from typing import List, Any

from bonsaicore.constructs import Operator,Predicate,Rule


class EvaluationResult:

    def __init__(self, output: dict, eval_order):
        self.output = output
        self.eval_order = eval_order


class EvaluationInput:

    def __init__(self, input: dict, namespace: str) -> None:
        self.input = input
        self.namespace = namespace

    @classmethod
    def build(cls, raw_input: dict):
        namespace = raw_input['namespace']
        input = {}
        for predicate in raw_input['predicates']:
            input[predicate['attribute_name']] = __get_type_casted_val__(predicate['type'], predicate['value'])

        return cls(input=input, namespace= namespace)

'''
Entrypoint for bonsai-dbrms , expected to be singleton across application container lifetime
initialised at startup
'''


class Bonsai:

    def __init__(self, raw_rule_set: dict):
        self.rules: [Rule] = self.setUp(raw_rule_set)
        print(self.rules)

    '''
    Sets up the inmemory rule tree 
    '''

    def setUp(self, raw_rule_set: dict):
        return self.__parse_raw_rules__(raw_rule_set)

    '''
    Processes the input to return matched rules as results,
    For now the last matched rule value is returned , as rule priorty support is yet to be added
    '''

    ## TODO : Add support for rule priorties
    def process(self, eval_input : EvaluationInput) -> EvaluationResult:
        result_set: set = set()
        prev_epoch_set_size = 0
        input = eval_input.input
        output = {}
        rule_set = self.rules[eval_input.namespace]

        while True:
            for rule in rule_set:
                does_match = rule.match(input)
                if does_match:
                    result_set.add(rule.id)
                    for rule_object in rule.result:
                        output[rule_object['attribute_name']] = rule_object['value']

            if prev_epoch_set_size == len(result_set):
                ## No rules matched in this epoch
                return EvaluationResult(output, list(result_set))

            prev_epoch_set_size = len(result_set)

    '''
    Marshals raw json to list of Rules(POJO)
    '''

    def __parse_raw_rules__(self, raw_rule_set: dict):
        rules = {}
        print(raw_rule_set)
        if raw_rule_set:

            for namespace, rulesets in raw_rule_set.items():
                rule_objs = []

                for rule_id, rule in rulesets.items():
                    predicates: [Predicate] = []

                    for predicate in rule['predicates']:
                        inferred_operator: Operator = Operator[predicate['operator']]
                        predicate_obj = Predicate(subject_attribute=predicate['attribute_name'],
                                                operator=inferred_operator,
                                                target_val=predicate['value'])
                        predicates.append(predicate_obj)

                    rule_objs.append(Rule(id=rule_id,
                                        predicates=predicates,
                                        result=rule['result']))

                rules[namespace] = rule_objs

        return rules


def __get_type_casted_val__(type: str, val: str):
    if type == "string":
        return val
    if type == "int":
        return int(val)

    raise Exception("Invalid type received as input attribute")


# if __name__ == "__main__":
#     raw_rule_set = {}

#     with open('sample_rule_set.json') as f:
#         raw_rule_set = json.load(f)

#     rule_evaluator = Bonsai(raw_rule_set)

    # raw_inp = {"namespace":"TaxSystem",
    #         "predicates": [
    #             {
    #             "attribute_name": "Province",
    #             "operator": "eq",
    #             "type": "string",
    #             "value": "Ontario"
    #             },
    #             {
    #             "attribute_name": "City",
    #             "operator": "eq",
    #             "type": "string",
    #             "value": "Toronto"
    #             }
    #         ]}

#     eval_input = EvaluationInput.build(raw_input= raw_inp)

#     result = rule_evaluator.process(eval_input= eval_input)
#     print(result.eval_order)
