from enum import Enum


class CategoriesEnum(Enum):
    SPACE = "space"
    AUTO = "auto"
    NATURE = "nature"

    # TODO: дополнить темами

    @property
    def comparator(self) -> dict:
        return {self.SPACE: 1, self.AUTO: 2, self.NATURE: 3}

    def to_value(self) -> int:
        return self.comparator[self]
