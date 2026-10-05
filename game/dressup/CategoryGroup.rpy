init python:
    class CategoryGroup:
        def __init__(self, name, priority = 0):
            self._name = name.capitalize().replace("_", " ")
            self._key = name
            self._priority = priority

        @property
        def name(self):
            return self._name

        @property
        def key(self):
            return self._key

        @property
        def priority(self):
            return self._priority

        def __eq__(self, other):
            if isinstance(other, str):
                return self.name == other
            if isinstance(other, CategoryGroup):
                return self.name == other.name
            return False