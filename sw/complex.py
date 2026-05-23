from __future__ import annotations
from fixed import Fixed

class Complex:
    real: float
    imag: float

    def __init__(self, r: float, i: float = 0):
        self.real = r
        self.imag = i


    def __mul__(self, other: Complex) -> Complex:
        result = Complex((self.real * other.real) - (self.imag * other.imag),
                       (self.real * other.imag) + (self.imag * other.real))
        return result

    
    def __add__(self, other: Complex) -> Complex:
        return Complex(self.real + other.real, self.imag + other.imag)
    

    def __sub__(self, other: Complex) -> Complex:
        return Complex(self.real - other.real, self.imag - other.imag)
    

    def __invert__(self) -> Complex:
        return Complex(self.real, -self.imag)


    def __abs__(self) -> float:
        return self.real ** 2 + self.imag ** 2
    

    def __repr__(self):
        return f'{self.real} + j{self.imag}'
    

    # def mag_sq(self) -> float:
    #     # print(self.real)
    #     return self.real ** 2 + self.imag ** 2