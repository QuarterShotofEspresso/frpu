from __future__ import annotations

class Fixed:

    _q:   tuple[int, int] = (4, 4)               # (Z bits, R bits)
    _pyl: int                                    # actual data
    _max: int =  2 ** ((_q[0] + _q[1]) // 2) - 1 # max value
    _min: int = -2 ** ((_q[0] + _q[1]) // 2)     # min value
    _ras: int =  2 ** (_q[1])

    
    def from_float(self, fpay: float) -> Fixed:
        return Fixed(int( (fpay * self._ras) // 1 ))

    
    def __init__(self, ipayload: int):
        self._pyl = ipayload


    def __add__(self, other: Fixed) -> Fixed:
        sum = self._pyl + other._pyl
        sum = self._max if sum > self._max else sum
        return Fixed(sum)
    
    
    def __sub__(self, other: Fixed) -> Fixed:
        sum = self._pyl - other._pyl
        sum = self._min if sum < self._min else sum
        return Fixed(sum)


    def __mul__(self, other: Fixed) -> Fixed:
        prod = (self._pyl * other._pyl) // self._ras
        prod = self._max if prod > self._max else prod
        return Fixed(prod)


    def __truediv__(self, other: float) -> Fixed:
        quot = (self._pyl * self._ras) // self.from_float(other)._pyl
        return Fixed(quot)


    def __neg__(self) -> Fixed:
        out = -self._pyl if self._min > self._pyl else self._min
        return Fixed(out)


    def __float__(self) -> float:
        return self._pyl / self._ras


    def __repr__(self):
        return f'{float(self)}'