from __future__ import annotations

class Fixed:

    _q:   tuple[int, int] = (4, 4)               # (Z bits, R bits)
    _pyl: int                                    # actual data
    _max: int =  2 ** (_q[0] + _q[1] - 1) - 1 # max value
    _min: int = -2 ** (_q[0] + _q[1] - 1)     # min value
    _ras: int =  2 ** (_q[1])

    
    @classmethod
    def from_float(cls, fpay: float) -> Fixed:
        out = int( (fpay * cls._ras) // 1 )
        return Fixed(cls._clamp(out))


    @classmethod
    def _clamp(cls, pyl: int) -> int:
        pyl = cls._max if pyl > cls._max else pyl
        pyl = cls._min if pyl < cls._min else pyl
        return pyl

    
    def __init__(self, ipayload: int):
        self._pyl = ipayload


    def __add__(self, other: Fixed) -> Fixed:
        out = self._pyl + other._pyl
        return Fixed(self._clamp(out))
    
    
    def __sub__(self, other: Fixed) -> Fixed:
        out = self._pyl - other._pyl
        return Fixed(self._clamp(out))


    def __mul__(self, other: Fixed) -> Fixed:
        out = (self._pyl * other._pyl) // self._ras
        return Fixed(self._clamp(out))


    def __truediv__(self, other: float) -> Fixed:
        out = (self._pyl * self._ras) // self.from_float(other)._pyl
        return Fixed(self._clamp(out))


    def __neg__(self) -> Fixed:
        out = -self._pyl
        return Fixed(self._clamp(out))


    def __float__(self) -> float:
        return self._pyl / self._ras


    def __repr__(self):
        return f'{float(self)}'