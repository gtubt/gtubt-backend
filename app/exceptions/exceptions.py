from django.utils.encoding import smart_text

from app.exceptions import codes


class PBaseException(Exception):
    code = codes.undefined

    def __init__(self, *args, **kwargs):
        code = self.code.get("code", "undefined")
        self.message = getattr(self.codes, "{}".format(code)).get("msg")
        self.params = kwargs.get("params")
        if self.params and isinstance(self.params, dict):
            self.message = smart_text(self.message).format(**self.params)
        if self.params and isinstance(self.params, (set, list, tuple)):
            self.message = smart_text(self.message).format(*self.params)

    @property
    def codes(self):
        return codes
