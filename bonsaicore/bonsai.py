import json

from typing import List

from bonsaicore.constructs import Operator,Predicate,Rule


'''
Entrypoint for bonsai-dbrms , expected to be singleton across application container lifetime
initialised at startup
'''
class Bonsai :

    def __init__(self,raw_rule_set:dict):
        self.rules : [Rule] = self.setUp(raw_rule_set)
        # print(self.rules)

    '''
    Sets up the inmemory rule tree 
    '''
    def setUp(self, raw_rule_set : dict) -> List[Rule]:
        return self.__parse_raw_rules__(raw_rule_set)

    '''
    Processes the input to return matched rules as results,
    For now the last matched rule value is returned , as rule priorty support is yet to be added
    '''
    ## TODO : Add support for rule priorties
    def process(self,input:dict) -> dict:
        result_set : set = set()
        prev_epoch_set_size = 0

        while True :
            for rule in self.rules :
                does_match = rule.match(input)
                if does_match :
                    result_set.add(rule.id)
                    for k,v in rule.result.items():
                        input[k] = v

            if prev_epoch_set_size == len(result_set):
                ## No rules matched in this epoch
                return input

            prev_epoch_set_size = len(result_set)

    '''
    Marshals raw json to list of Rules object
    '''
    def __parse_raw_rules__(self,raw_rule_set : dict):
        rules = []

        for raw_rule in raw_rule_set['rules']:
            predicates: [Predicate] = []
            for predicate in raw_rule['predicates']:
                inferred_operator: Operator = Operator[predicate['operator']]
                predicate_obj = Predicate(subject_attribute=predicate['attribute_name'],
                                          operator=inferred_operator,
                                          target_val=predicate['value'])
                predicates.append(predicate_obj)

            rules.append(Rule(id=raw_rule['id'],
                              predicates=predicates,
                              result=raw_rule['result']))
        return rules

if __name__ == "__main__":
    raw_rule_set = {}

    with open('sample_rule_set.json') as f:
        raw_rule_set = json.load(f)

    rule_evaluator = Bonsai(raw_rule_set)
    result = rule_evaluator.process({'Province' : "Ontario",
                            'City' : "Toronto"})
    print(result)
