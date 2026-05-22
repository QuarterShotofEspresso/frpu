#!/opt/homebrew/bin/python3

from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from complex import Complex
import argparse

width, height = 480, 272
# resolution = 25


def _map(x: int, ei: int, so: float, eo: float) -> float:
    return ((eo - so) * x / ei) + so


squeeze: float = 0.55
scale: int = 255


def wine_color_grade(z: Complex) -> int:
    if abs(z) - 4 > 0:
        return 0
    else:
        return int( scale * (2.0 ** -(squeeze * abs(abs(z) - 4))) )


def std_color_grade(z: Complex) -> int:
    if abs(z) - 4 > 0:
        return 0
    else:
        return 255


def gen_frame_points(anchor_point: Complex, radius: Complex) -> tuple[Complex, Complex]:
    return (anchor_point + radius, anchor_point - radius)


def gen_pixel_domain(startp: float, endp: float) -> list[float]:
    return [_map(i, width, startp, endp) for i in range(width)]


def gen_pixel_range(startp: float, endp: float) -> list[float]:
    return [_map(i, height, startp, endp) for i in range(height)]


def compute_mandelbrot(c: Complex, resolution: int) -> Complex:
    z = Complex(0)
    for _ in range(resolution):
        z = (z * z) + c
        if abs(z) > 4:
            return z
    return z


def convert_to_pixel(z: Complex) -> bytes:
    # return bytes([wine_color_grade(z), 0, 0])
    return bytes([std_color_grade(z), 0, 0])


def write_img_to_file(img: bytearray, filename: str):
    with open(f'{filename}.ppm', 'wb') as f:
        f.write(f'P6\n{width} {height}\n255\n'.encode())
        f.write(img)


def comp_row(row: list[Complex], resolution: int) -> bytes:
    return b''.join(convert_to_pixel(compute_mandelbrot(p, resolution)) for p in row)


def gen_frame(anchor: Complex, radius: Complex, resolution: int) -> bytearray:
    start_point, end_point = gen_frame_points(anchor, radius)
    frame_domain = gen_pixel_domain(start_point.real, end_point.real)
    frame_range  = gen_pixel_range(start_point.imag, end_point.imag)
    frame = bytearray()
    with ProcessPoolExecutor() as exec:
        rows = [[Complex(dp, rp) for dp in frame_domain] for rp in frame_range]
        futures = [exec.submit(comp_row, row, resolution) for row in rows]
        for f in futures:
            frame += f.result()
    return frame


if __name__ == '__main__':
    corner_point = Complex(-2, 1)
    center_anchor = Complex(-0.5, 0)

    radius = corner_point - center_anchor

    target_anchor = Complex(-0.75, 0.10) # seahorse valley
    # target_anchor = Complex(-2.00, 0.00) # Misiurewicz Points
    # target_anchor = Complex(-0.10, 0.83) # Triple Spiral Valley

    total_frames = 100

    resolution = 25
    print(f'making movie (len={total_frames})', end='', flush=True)
    for i in range(total_frames):
        img = gen_frame(target_anchor, radius, resolution)
        write_img_to_file(img, f'out/mandel-{i}')
        print('.', end='', flush=True)
        radius = Complex(0.9) * radius
        # resolution += 1
    print('done')
