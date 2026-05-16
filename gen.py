#!/opt/homebrew/bin/python3

from __future__ import annotations
from complex import Complex
import argparse

width, height = 480, 272
resolution = 25


def _map(x: int, ei: int, so: float, eo: float) -> float:
    return ((eo - so) * x / ei) + so


squeeze: float = 0.55
scale: int = 255


def wine_color_grade(z: Complex) -> int:
    if abs(z) - 4 > 0:
        return 0
    else:
        return int( scale * (2.0 ** -(squeeze * abs(abs(z) - 4))) )


def gen_frame_points(anchor_point: Complex, radius: Complex) -> tuple[Complex, Complex]:
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


def gen_frame(anchor: Complex, radius: Complex) -> bytearray:
    start_point, end_point = gen_frame_points(anchor, radius)
    frame_domain = gen_pixel_domain(start_point.real, end_point.real)
    frame_range  = gen_pixel_range(start_point.imag, end_point.imag)
    frame = bytearray()
    for rp in frame_range:
        for dp in frame_domain:
            z = compute_mandelbrot(Complex(dp, rp))
            frame += convert_to_pixel(z)
    
    return frame

corner_point = Complex(-2, 1)
center_anchor = Complex(-0.5, 0)

radius = corner_point - center_anchor

target_anchor = Complex(-0.75, 0.1)

total_frames = 20

print(f'making movie (len={total_frames})', end='', flush=True)
for i in range(total_frames):
    img = gen_frame(target_anchor, radius)
    write_img_to_file(img, f'out/mandel-{i}')
    print('.', end='', flush=True)
    radius = Complex(0.9) * radius
print('done')
