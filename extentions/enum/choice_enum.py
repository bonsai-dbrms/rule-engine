import inspect


class ChoiceEnum(object):
    @classmethod
    def choices(cls):
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        choices = tuple((m[1], m[0]) for m in members if not(m[0][:2] == '__'))
        return choices

    @classmethod
    def to_dict(cls):
        return dict(cls.__dict__)
