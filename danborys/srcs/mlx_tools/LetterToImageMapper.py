from typing import Tuple
from srcs.mlx_tools.BaseMLX import MlxVarWithLetters
from srcs.mlx_tools.mlx_errors import (
    ImgError
)
from srcs.mlx_tools.ImageOperations import ImgData
from srcs.mlx_tools.ImageOperations import ImageOperations


class LetterToImageMapper:
    def __init__(self, mlx: MlxVarWithLetters) -> None:
        self.mlx = mlx
        self.image = "images/alphabets.xpm"
        self.letter_per_row = 9
        self.cap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.small = "abcdefghijklmnopqrstuvwxyz"
        self.num = "0123456789"
        self.symbols = ".,;:_#'!\"/?<>%&*()"
        self.mlx.letter_img = ImageOperations.xmp_to_img(self.mlx, self.image)

    def create_map(self):
        w = 60  # Horizontal spacing between each letter
        h = 80  # Vertical spacing between each letter
        try:
            # all this parameters depends on the xpm image file
            # and need manual selection at first
            self.extract_different_letter_types(
                self.cap, 55, 45, 0, 30, w, h, 0)
            self.extract_different_letter_types(
                self.small, 55, 45, 0, 30, w, h, 264)
            self.extract_different_letter_types(
                self.num, 55, 45, 0, 30, w, h, 528)
            self.extract_different_letter_types(
                self.symbols, 55, 45, 0, 30, w, h, 712)
            self.mlx.base_letter_map[" "] = ImageOperations.generate_blank_image(
                self.mlx, 30, 50)
        except ImgError as e:
            raise ImgError(f"{type(e).__name__}: {e}")

    def extract_different_letter_types(self, symbols: str, crop_w: int,
                                       crop_h: int, x_off: int, y_off: int,
                                       w: int, h: int, vertical_off: int):
        for id, letter in enumerate(symbols):
            x = id % self.letter_per_row
            y = id // self.letter_per_row
            new_x_off, width = self.extract_letter_width(
                self.mlx.letter_img, (
                    w * x + 2, h * y + y_off + vertical_off), crop_h, crop_w)
            # print(f"{letter}, x: {x}, off: {new_x_off}, w: {width}")
            self.crop_sub_image_from_image(
                letter, width, crop_h,
                (w * x + 2 + new_x_off, h * y + y_off + vertical_off))

    def extract_letter_width(self, img: ImgData, center: Tuple,
                             h: int, w: int) -> Tuple[int, int]:
        start_x, start_y = center
        # print(f"Shared: {start_x, start_x + w}")
        left_width, right_width = img.w + 10, 0
        for y in range(start_y, start_y + h):
            x = start_x
            pos = y * img.sl + 4 * x
            # for x in range(start_x, start_x + w):
            while img.data is not None and (
                img.data[pos + 1] == 0 and
                img.data[pos + 2] == 0 and
                    img.data[pos + 3] == 0) and x < start_x + w:
                x += 1
                pos = y * img.sl + 4 * x
            if left_width > x:
                left_width = x

            x = start_x + w - 2
            pos = y * img.sl + 4 * x
            while img.data is not None and (
                img.data[pos + 1] == 0 and
                img.data[pos + 2] == 0 and
                    img.data[pos + 3] == 0) and x > start_x:
                x -= 1
                pos = y * img.sl + 4 * x
            if right_width < x:
                right_width = x
        left_width, right_width = left_width - 2, right_width + 2
        return (left_width - start_x, (right_width - left_width))

    def crop_sub_image_from_image(self, key: str, w: int, h: int,
                                  center: Tuple, color=0xFFFFFFFF,
                                  bg_color=0x00000000):
        self.mlx.base_letter_map[key] = ImageOperations.generate_blank_image(
            self.mlx, w, h)
        ImageOperations.crop_img(self.mlx.base_letter_map[key],
                                 self.mlx.letter_img, center)
