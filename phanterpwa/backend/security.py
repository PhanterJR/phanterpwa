from itsdangerous import (
    URLSafeSerializer,
    SignatureExpired,
    BadSignature
)
from datetime import (
    datetime,
    timedelta
)


class Serialize():
    def __init__(self, secret, expire_in=315576000):
        self.secret = secret
        self.expire_in = expire_in

    @property
    def expire_in(self):
        return self._expire_in

    @expire_in.setter
    def expire_in(self, value):
        self._expire_in = 315576000
        try:
            self._expire_in = int(value)
        except Exception:
            self._expire_in = 315576000

    def dumps(self, value):
        s = URLSafeSerializer(self.secret)
        new_value = {
            "expire_in": str(datetime.now() + timedelta(seconds=self.expire_in)),
            "value": value
        }
        return s.dumps(new_value)

    def loads(self, value, datetime_expire=None):
        s = URLSafeSerializer(self.secret)
        j = s.loads(value)
        v = j.get("value")
        e = j.get("expire_in")
        expire_in = datetime.fromisoformat(e)
        if datetime_expire is None:
            datetime_expire = datetime.now()
        if datetime_expire > expire_in:
            raise SignatureExpired("The token has expired")
        else:
            return v
