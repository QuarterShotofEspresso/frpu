#!/opt/homebrew/bin/python3

from __future__ import annotations
from complex import Complex
import argparse

width, height = 480, 272
resolution = 15

ref_frame_point = Complex(-2, 1)
default_anchor = Complex(-0.5, 0)

anchor_point = Complex(-0.75, 0.1)
adj_frame_point: Complex = ref_frame_point + anchor_point
# radius: Complex = adj_frame_point - anchor_point


def _map(x: int, ei: int, so: float, eo: float) -> float:
    return ((eo - so) * x / ei) + so

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


squeeze: float = 0.55
scale: int = 255

def mand(c: Complex, resolution: int) -> tuple[bool, Complex]:
    z: Complex = Complex(0)
    for _ in range(resolution):
        z = (z * z) + c
        if abs(z) > 4:
            return (False, z)
    return (True, z)

def wine_color_grade(z: Complex) -> int:
    if abs(z) - 4 > 0:
        return 0
    else:
        return int( scale * (2.0 ** -(squeeze * abs(abs(z) - 4))) )

def gen_mand_pixel(c: Complex, resolution: int) -> bytes:
    is_member, vec = mand(c, resolution)
    grade = wine_color_grade(vec)
    if is_member:
        return bytes([int(grade), 0, 0])
    else:
        return b'\x00\x00\x00'


# def gen_frame(resolution: int, bounds: dict[str, list[float]], filename: str = 'mandel'):
#     with open(f'{filename}.ppm', 'wb') as f:
#         f.write(f'P6\n{width} {height}\n255\n'.encode())
#         row = bytearray()
#         for i in bounds['range']:
#             for j in bounds['domain']:
#                 row += gen_mand_pixel(Complex(j, i), resolution)
#         f.write(row)

# def gen_movie(resolution: int, filename: str = 'mandel'):
#     center_point = (-0.75, 0.1)
#     total_frames = 20

#     dom = (-2.0 + center_point[0], 1.0 + center_point[0])
#     ran = (-1.0 + center_point[1], 1.0 + center_point[1])
#     bounds = {'domain_start': dom[0], 'domain_end': dom[1], 'range_start': ran[0], 'range_end': ran[1]}

#     print(f'making movie (len={total_frames})', end='', flush=True)
#     for i in range(total_frames):
#         print('.', end='', flush=True)
#         region = compute_pixel_points(bounds)
#         gen_frame(resolution, region, f'out/{filename}-{i}')
#         bounds = center_zoom(bounds, 0.1)
#     print('done.')


def gen_frame_points(radius: Complex) -> tuple[Complex, Complex]:
    return (anchor_point + radius, anchor_point - radius)

def gen_pixel_domain(startp: float, endp: float) -> list[float]:
    return [_map(i, width, startp, endp) for i in range(width)]

def gen_pixel_range(startp: float, endp: float) -> list[float]:
    return [_map(i, height, startp, endp) for i in range(height)]

def compute_mandelbrot(c: Complex) -> Complex:
    z = Complex(0)
    for _ in range(resolution):
        z = (z * z) + c
        if abs(z) > 4:
            return z
    return z


def convert_to_pixel(z: Complex) -> bytes:
    return bytes([wine_color_grade(z), 0, 0])


def write_img_to_file(img: bytearray, filename: str):
    with open(f'{filename}.ppm', 'wb') as f:
        f.write(f'P6\n{width} {height}\n255\n'.encode())
        f.write(img) 


def gen_frame(radius: Complex) -> bytearray:
    start_point, end_point = gen_frame_points(radius)
    print(start_point, end_point)
    frame_domain = gen_pixel_domain(start_point.real, end_point.real)
    frame_range  = gen_pixel_range(start_point.imag, end_point.imag)
    frame = bytearray()
    for rp in frame_range:
        for dp in frame_domain:
            z = compute_mandelbrot(Complex(dp, rp))
            frame += convert_to_pixel(z)
    
    return frame


# def center_zoom(bounds: dict[str, float], dz: float) -> dict[str, float]:
#     xs = bounds['domain_start']
#     xe = bounds['domain_end']
#     ys = bounds['range_start']
#     ye = bounds['range_end']

#     ar = (ys - ye)/(xe - xs)

#     xsp = xs + dz
#     xep = xe - dz
#     ysp = ys - (ar * dz)
#     yep = ye + (ar * dz)

#     return {'domain_start': xsp, 'domain_end': xep, 'range_start': ysp, 'range_end': yep}


img = gen_frame(ref_frame_point - default_anchor)
write_img_to_file(img, 'out/mandel-test')
# gen_movie(25, 'mandel')

# center_point = (-0.75, 0.1)

# dom = (-2.0 + center_point[0], 1.0 + center_point[0])
# ran = (-1.0 + center_point[1], 1.0 + center_point[1])

# print(dom[0], ran[1])
# print(dom[1], ran[0])
# for i in range(5, 51, 5):
#     gen_frame(i, f'{i}')