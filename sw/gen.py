#!.venv/bin/python3

from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from rich.progress import track
from complex import Complex
from fixed import Fixed
import argparse

FRAME_WIDTH, FRAME_HEIGHT = 480, 272

class ComplexFrame:
    start_frame: Complex
    dx: Complex
    dy: Complex

    def __init__(self, start_frame: Complex, dx: Complex, dy: Complex):
        self.start_frame = start_frame
        self.dx = dx
        self.dy = dy

    def zoom(self, zoom_rate: Complex):
        self.start_frame *= zoom_rate
        self.dx *= zoom_rate
        self.dy *= zoom_rate


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


def compute_mandelbrot(c: Complex, resolution: int) -> Complex:
    z = Complex(Fixed(0))
    for _ in range(resolution):
        if abs(z) > 4:
            return z
        z = (z * z) + c
    return z


def convert_to_pixel(z: Complex) -> bytes:
    # return bytes([wine_color_grade(z), 0, 0])
    return bytes([std_color_grade(z), 0, 0])


def write_img_to_file(img: bytearray, filename: str):
    with open(f'{filename}.ppm', 'wb') as f:
        f.write(f'P6\n{FRAME_WIDTH} {FRAME_HEIGHT}\n255\n'.encode())
        f.write(img)


def comp_row(row: list[Complex], resolution: int) -> bytes:
    return b''.join(convert_to_pixel(compute_mandelbrot(p, resolution)) for p in row)


# def gen_frame(anchor: Complex, radius: Complex, resolution: int) -> bytearray:
def gen_frame(start: Complex, dx: Complex, dy: Complex, resolution: int) -> bytearray:
    frame = bytearray()
    with ProcessPoolExecutor() as exec:
        rows = [[start + (dx * Complex(Fixed.from_float(j)) + dy * Complex(Fixed.from_float(i))) for j in range(FRAME_WIDTH)] for i in range(FRAME_HEIGHT)]
        futures = [exec.submit(comp_row, row, resolution) for row in rows]
        for f in futures:
            frame += f.result()
    return frame


if __name__ == '__main__':
    total_frames = 200
    # resolutionf = 9.4
    # resolution: int = int(resolutionf)
    resolution: int = 15
    zoom_rate = Complex(Fixed.from_float(0.95))

    origin_start_frame = Complex(Fixed.from_float(-2), Fixed.from_float(1))
    origin_anchor = Complex(Fixed.from_float(-0.5), Fixed.from_float(0))

    radius: Complex = origin_start_frame - origin_anchor
    print(f"radius: {radius}")

    origin_end_scanline: Complex = origin_anchor + radius.rflv()
    origin_last_scanline: Complex = origin_anchor + radius.rflh()

    frame_width: Complex = origin_end_scanline - origin_start_frame
    frame_height: Complex = origin_last_scanline - origin_start_frame
    print(f'frame width: {frame_width}\nframe height: {frame_height}')

    dx: Complex = frame_width / float(FRAME_WIDTH)
    dy: Complex = frame_height / float(FRAME_HEIGHT)
    print(f"dx: {dx}\ndy: {dy}")

    target_anchor = Complex(Fixed.from_float(-0.7445), Fixed.from_float(0.10025)) # seahorse valley
    # target_anchor = Complex(-2.00, 0.00) # Misiurewicz Points
    # target_anchor = Complex(-0.10, 0.83) # Triple Spiral Valley

    target_start_frame = target_anchor + radius

    for i in track(range(total_frames), description=f"Rendering {total_frames} frames..."):
        img = gen_frame(target_start_frame, dx, dy, resolution)
        # img = gen_frame(target_anchor, radius, resolution)
        write_img_to_file(img, f'out/mandel-{i}-{resolution}')
        radius *= zoom_rate
        dx *= zoom_rate
        dy *= zoom_rate
        target_start_frame = target_anchor + radius
        # resolutionf += 1
        # resolution = int(resolutionf)
        resolution += 1
    print('done')
