
from typing import Any
from bonsaicore.constructs import Operator, OPERATION_EVALUATOR_MAP

class Predicate:

    def __init__(self, subject_attribute : str ,operator: Operator, target_val: Any) -> None:
        self.attribute_name = subject_attribute
        self.operator: Operator = operator
        self.target_val : Any = target_val

    def evaluate(self,input_val) -> bool:
        return OPERATION_EVALUATOR_MAP[self.operator](input_val,self.target_val)
