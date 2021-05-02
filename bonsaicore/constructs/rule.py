from bonsaicore.constructs import Predicate
'''
Defines any rule , with corresponding rule id and list of predicates
'''
class Rule:

    def __init__(self, id: str, predicates: [Predicate], result: dict) -> None:
        self.id = id

        self.predicate_mapping: dict[str, Predicate] = {}

        for predicate in predicates:
            self.predicate_mapping[predicate.attribute_name] = predicate

        self.result = result

    def match(self, input_val: dict) -> bool:
        for attribute in  self.predicate_mapping.keys():

            if attribute not in input_val:
                return False

            res = self.predicate_mapping[attribute].evaluate(input_val[attribute])
            if not res:
                return False

        return True
