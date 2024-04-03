from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def from_string(cls, string_value):
        string_value = string_value.upper()
        for item in cls:
            if item.name == string_value:
                return item
        raise ValueError(f"{string_value} is not a valid value for {cls.__name__}")

    @classmethod
    def get_day_by_number(cls, number):
        for day in cls:
            if day.value == number:
                return day.name
        return None


class DayOfWeek(BaseEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Gender(BaseEnum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
