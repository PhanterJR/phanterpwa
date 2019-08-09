from .tools import check_activation_code


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
