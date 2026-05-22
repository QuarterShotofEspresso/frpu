from __future__ import annotations

class Fixed:
    _bp: int = 20   # bits before binary point
    _pyl: int       # actual data

    
    def _to_fix(self, x: float) -> int:
        return x * (2**self._bp) // (2**self._bp)


    def __init__(self, payload: float):
        self._pyl = self._to_fix(payload)
    

    def __add__(self, other: Fixed):
        return self._pyl + other._pyl
    
    
    def __sub__(self, other: Fixed):
        return self._pyl - other._pyl


    def __mul__(self, other: Fixed):
        return (self._pyl * other._pyl) / (2**self._pyl)