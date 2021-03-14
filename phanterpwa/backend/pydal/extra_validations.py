from datetime import (
    datetime,
    timedelta
)
from passlib.hash import pbkdf2_sha512
from phanterpwa.tools import check_activation_code


class IS_ACTIVATION_CODE:
    def __init__(self, size=6, error_message='error'):
        self.e = error_message
        self.s = size

    def __call__(self, value, record_id=None):
        if check_activation_code(value, self.s):
            return (value, None)
        return (value, self.e)

    def formatter(self, value):
        return value


class HASH_MATCH_WITH_PASSWORD:
    def __init__(self, password, error_message='password does not mach with hash'):
        self.e = error_message
        self.password = password

    def __call__(self, value, record_id=None):
        if pbkdf2_sha512.verify(value, self.password):
            return (value, None)
        return (value, self.e)

    def formatter(self, value):
        return value


class PASSWORD_MATCH_WITH_HASH:
    def __init__(self, hash_password, error_message='password does not mach with hash'):
        self.e = error_message
        self.hash_password = hash_password

    def __call__(self, value, record_id=None):
        if pbkdf2_sha512.verify(value, self.hash_password):
            return (value, None)
        return (value, self.e)

    def formatter(self, value):
        return value

class VALID_PASSWORD:
    def __init__(self, user_record, error_message='password does not mach with hash'):
        self.e = error_message
        self.user_record = user_record

    def __call__(self, value, record_id=None):
        user = self.user_record
        result = pbkdf2_sha512.verify(value, user.password_hash)
        if not result and user.temporary_password_hash:
            result = pbkdf2_sha512.verify(value, user.temporary_password_hash)
        if result:
            return (value, None)    
        return (value, value)

    def formatter(self, value):
        return value