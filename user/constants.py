from util.extended_enum import ExtendedEnum


class UserType(ExtendedEnum):
    ADMIN = 'admin'
    DATA_ENTRY = 'data_entry'
    USER = 'user'