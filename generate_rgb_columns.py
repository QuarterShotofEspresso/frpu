from __future__ import annotations
import argparse

width, height = 480, 272
resolution = 15

def compute_pixel_points(bounds: dict[str, float]) -> dict[str, list[float]]:
    xs = bounds['domain_start']
    xe = bounds['domain_end']
    ys = bounds['range_start']
    ye = bounds['range_end']
    map_domain: list[float] = [((xe - xs) * i / width) + xs for i in range(width)]
    map_range: list[float] = [((ye - ys) * i / height) + ys for i in range(height)]
    return {'domain': map_domain, 'range': map_range}

# class Fixed:
#     width: int = 32
#     iwid: int = 2

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
    
    def __repr__(self):
        return f'{self.real} + j{self.imag}'
    
    def mag_sq(self) -> float:
        # print(self.real)
        return self.real ** 2 + self.imag ** 2

squeeze: float = 0.55
scale: int = 255

def mand(c: Complex, resolution: int) -> tuple[bool, int]:
    z: Complex = Complex(0);
    for i in range(resolution):
        z = (z * z) + c
        if z.mag_sq() > 4:
            # return (False, scale * (2.0 ** -(squeeze * abs(z.mag_sq() - 4))))
            return (False, scale * (2.0 ** -(squeeze * abs(z.mag_sq() - 4))))
    return (True, scale * (2.0 ** -(squeeze * abs(z.mag_sq() - 4))))
    # return (True, scale * (2.0 ** -(squeeze * abs(z.mag_sq() - 4))))
    # return (z.mag_sq() > 4)

def fancy_color(z: Complex) -> int:
    return int(  )

def gen_mand_pixel(c: Complex, resolution: int) -> bytes:
    red, grade = mand(c, resolution)
    if red:
        # return b'\xff\x00\x00'
        return bytes([int(grade), 0, 0])
    else:
        # return bytes([0, 0, int(grade)])
        # return bytes([0, 0, int(grade)])
        # return b'\x00\x00\xff'
        return b'\x00\x00\x00'


def gen_frame(resolution: int, bounds: dict[str, list[float]], filename: str = 'mandel'):
    with open(f'{filename}.ppm', 'wb') as f:
        f.write(f'P6\n{width} {height}\n255\n'.encode())
        row = bytearray()
        for i in bounds['range']:
            for j in bounds['domain']:
                row += gen_mand_pixel(Complex(j, i), resolution)
        f.write(row * height)

def gen_movie(resolution: int, filename: str = 'mandel'):
    center_point = (-0.75, 0.1)
    total_frames = 20

    dom = (-2.0 + center_point[0], 1.0 + center_point[0])
    ran = (-1.0 + center_point[1], 1.0 + center_point[1])
    bounds = {'domain_start': dom[0], 'domain_end': dom[1], 'range_start': ran[0], 'range_end': ran[1]}

    print(f'making movie (len={total_frames})', end='', flush=True)
    for i in range(total_frames):
        print('.', end='', flush=True)
        region = compute_pixel_points(bounds)
        gen_frame(resolution, region, f'out/{filename}-{i}')
        bounds = center_zoom(bounds, 0.1)
    print('done.')


def center_zoom(bounds: dict[str, float], dz: float) -> dict[str, float]:
    xs = bounds['domain_start']
    xe = bounds['domain_end']
    ys = bounds['range_start']
    ye = bounds['range_end']

    ar = (ys - ye)/(xe - xs)

    xsp = xs + dz
    xep = xe - dz
    ysp = ys - (ar * dz)
    yep = ye + (ar * dz)

    return {'domain_start': xsp, 'domain_end': xep, 'range_start': ysp, 'range_end': yep}

gen_movie(25, 'mandel')

# for i in range(5, 51, 5):
#     gen_frame(i, f'{i}')