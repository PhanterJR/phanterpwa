from phanterpwa.tools import check_activation_code
from phanterpwa.tools import check_password_hash


class IS_ACTIVATION_CODE:
    def __init__(self, size=6, error_message='error'):
        self.e = error_message
        self.s = size

    def __call__(self, value):
        if check_activation_code(value, self.s):
            return (value, None)
        return (value, self.e)

    def formatter(self, value):
        return value


class HASH_MATCH_WITH_PASSWORD:
    def __init__(self, password, error_message='password does not mach with hash'):
        self.e = error_message
        self.password = password

    def __call__(self, value):
        if check_password_hash(self.password, value):
            return (value, None)
        return (value, self.e)

    def formatter(self, value):
        return value


class PASSWORD_MATCH_WITH_HASH:
    def __init__(self, hash_password, error_message='password does not mach with hash'):
        self.e = error_message
        self.hash_password = hash_password

    def __call__(self, value):
        if check_password_hash(self.hash_password, value):
            return (value, None)
        return (value, self.e)

    def formatter(self, value):
        return value
