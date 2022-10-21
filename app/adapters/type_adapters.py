from sqlalchemy import String
from sqlalchemy.types import TypeDecorator


class StringifiedArray(TypeDecorator):
    impl = String(length=255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = ",".join(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.split(",")
        return value
