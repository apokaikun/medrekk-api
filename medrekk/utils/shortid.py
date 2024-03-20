from string import ascii_letters, digits
from time import time_ns


class ShortID:
    def __init__(self):
        self._last_ts = time_ns()
        self._alpha = ascii_letters + digits

    def shortid(self) -> str:
        _now = time_ns()
        while(_now <= self._last_ts):
            _now = time_ns()
        self._last_ts = _now
        return self._int_to_alpha(_now)
    
    
    def _int_to_alpha(self, t):
        base = len(self._alpha)
        q = t
        alpha = ""
        while q:
            q, r = divmod(q, base)
            alpha += self._alpha[r]

        return alpha[::-1]
        
    def _alpha_to_int(self, s):
        num = 0
        base = len(self._alpha)
        for c in s:
            num = num * base + self._alpha.index(c)
        return num
    
id_gen = ShortID()
shortid = id_gen.shortid