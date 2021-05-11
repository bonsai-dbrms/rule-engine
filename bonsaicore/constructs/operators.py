from typing import Callable
from enum import Enum, auto

# TODO : add support for floating point numbers

class OperationEvaluationException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Operator(Enum):
    contains = auto()
    range = auto()
    lt = auto()
    lte = auto()
    gt = auto()
    gte = auto()
    eq = auto()

'''
Evaluates contains operations 
called as eval_contains(input_str,target_str)
'''
def eval_contains(*args):
    if len(args) != 2 :
        raise OperationEvaluationException("Contains operation requires exactly two params")

    for string in args:
        if type(string) is not str:
            raise OperationEvaluationException("Contains operation requires arguments to be of str type")

    return args[0] in args[1]

'''
Evaluates contains operations 
called as eval_contains(input_val,target_range:tuple)
this is inclusive of both start and end of target range
'''
def eval_range(*args):
    if len(args) != 2 :
        raise OperationEvaluationException("range operation requires exactly two params")

    if type(args[0]) is not int :
        raise OperationEvaluationException("range operation requires first argument to be the integer type")

    if type(args[1]) is not tuple :
        raise OperationEvaluationException("range operation requires first argument to be tuple type")

    if len(tuple(args[1])) != 2 :
        raise OperationEvaluationException("tuple argument must be of length 2, specifying start and end")

    return args[0] >= args[1][0] and args[0] <= args[1][1]


def eval_eq(*args):
    if len(args) != 2 :
        raise OperationEvaluationException("equality operation requires exactly two params")

    if type(args[0]) is not type(args[1]):
        raise OperationEvaluationException("equality operation requires params of same type")

    return args[0] == args[1]

def eval_gt(*args):
    if len(args) != 2 :
        raise OperationEvaluationException("greater than operation requires exactly two params")

    if type(args[0]) is not type(args[1]):
        raise OperationEvaluationException("greater than operation requires params of same type")

    return args[0] > args[1]

def eval_gte(*args):
    if len(args) != 2 :
        raise OperationEvaluationException("greater than equal operation requires exactly two params")

    if type(args[0]) is not type(args[1]):
        raise OperationEvaluationException("greater than equal operation requires params of same type")

    return args[0] >= args[1]

def eval_lt(*args):
    if len(args) != 2 :
        raise OperationEvaluationException("less than operation requires exactly two params")

    if type(args[0]) is not type(args[1]):
        raise OperationEvaluationException("less than operation requires params of same type")

    return args[0] < args[1]

def eval_lte(*args):
    if len(args) != 2 :
        raise OperationEvaluationException("less than equal operation requires exactly two params")

    if type(args[0]) is not type(args[1]):
        raise OperationEvaluationException("less than equal operation requires params of same type")

    return args[0] < args[1]

OPERATION_EVALUATOR_MAP = {
    Operator.contains : eval_contains,
    Operator.range : eval_range,
    Operator.eq : eval_eq,
    Operator.gt : eval_gt,
    Operator.gte : eval_gte,
    Operator.lt : eval_lt,
    Operator.lte : eval_lte
}

if __name__ == "__main__":
    print(Operator['eq'])
