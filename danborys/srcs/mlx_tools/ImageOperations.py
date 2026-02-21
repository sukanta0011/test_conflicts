from __future__ import annotations
from typing import List, Tuple, Protocol, Dict, TYPE_CHECKING
from srcs.mlx_tools.mlx_errors import (
    ImgError,
    ParametersError,
    InitializationError,
    OperationError
)
if TYPE_CHECKING:
    from srcs.mlx_tools.BaseMLX import MlxVar


class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.w = 0
        self.h = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


class ImageOperations:
    @staticmethod
    def generate_blank_image(mlx: MlxVar, w: int, h: int) -> ImgData:
        if w <= 0 or h <= 0:
            raise ParametersError(
                "ParametersError: Blank image generation failed"
                f"w and h has to be positive ({w}, {h})")
        if not isinstance(w, int) or not isinstance(h, int):
            raise ParametersError(
                "Blank image generation failed"
                f"w and h has to be integer ({w}, {h})")
        new_img = ImgData()
        new_img.h = int(h)
        new_img.w = int(w)
        try:
            new_img.img = mlx.mlx.mlx_new_image(
                mlx.mlx_ptr, new_img.w, new_img.h)
            new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
                mlx.mlx.mlx_get_data_addr(new_img.img)
            return new_img
        except Exception as e:
            raise InitializationError(
                f"Blank image generation failed: {e}"
            )

    @staticmethod
    def xmp_to_img(mlx: MlxVar, image_loc: str) -> ImgData:
        try:
            img = ImgData()
            result = mlx.mlx.mlx_xpm_file_to_image(mlx.mlx_ptr, image_loc)
            img.img, img.w, img.h = result
            img.data, img.bpp, img.sl, img.iformat = \
                mlx.mlx.mlx_get_data_addr(img.img)
            return img
        except Exception as e:
            raise InitializationError(
                f"Unable to load xmp image {image_loc}. {e}"
            )

    @staticmethod
    def copy_img(dest: ImgData, src: ImgData, center: Tuple[int, int]) -> None:
        start_x, start_y = center
        if not isinstance(start_x, int) or not isinstance(start_y, int):
            raise ParametersError(
                "Copying image failed, center coordinate need to be "
                f"integer ({center})")
        if (0 <= start_x < dest.w) and (0 <= start_y < dest.h):
            if start_x + src.w > dest.w:
                w = dest.w - start_x
                sl = w
            else:
                w = src.w
                sl = src.sl
            if start_y + src.h > dest.h:
                h = dest.h - start_y
            else:
                h = src.h
        else:
            raise ParametersError(
                "(fn :ImageOperations.copy_img) "
                "Source image dimension is bigger than destination image")
        for y in range(h):
            dest_start = (start_y + y) * dest.sl + (4 * start_x)
            dest_end = dest_start + (4 * w)
            src_start = y * sl
            src_end = src_start + (w * 4)
            if dest.data is not None and src.data is not None:
                dest.data[dest_start:dest_end] = src.data[src_start:src_end]
            else:
                raise OperationError(
                    "Cropping failed, The dest or src image is empty"
                )

    @staticmethod
    def crop_img(dest: ImgData, src: ImgData, center: Tuple) -> None:
        start_x, start_y = center
        if not isinstance(start_x, int) or not isinstance(start_y, int):
            raise ParametersError(
                "Cropping image failed, center coordinate need to be "
                f"integer ({center})")
        if (0 <= start_x < src.w) and (0 <= start_y < src.h):
            if start_x + dest.w > src.w:
                w = src.w - start_x
                sl = w
            else:
                w = dest.w
                sl = dest.sl
            if start_y + dest.h > src.h:
                h = src.h - start_y
            else:
                h = dest.h
        else:
            raise ParametersError(
                "Source image dimension is bigger than destination image")
        for y in range(h):
            dest_start = y * sl
            dest_end = dest_start + (4 * w)
            src_start = (start_y + y) * src.sl + (4 * start_x)
            src_end = src_start + (4 * w)
            if dest.data is not None and src.data is not None:
                dest.data[dest_start:dest_end] = src.data[src_start:src_end]
            else:
                raise OperationError(
                    "Cropping failed, The dest or src image is empty"
                )

    @staticmethod
    def set_pixel(img: ImgData, center: int | Tuple, color=0xFFFFFFFF) -> None:
        if isinstance(center, int):
            # print(f"one position: {center}")
            pos = center
            if pos >= (img.w * img.h * 4) or pos < 0:
                raise ParametersError(
                    f"Unable to set pixel, {pos}, is out of range of "
                    "the image dimensions"
                )
        elif isinstance(center, tuple):
            if len(center) == 2:
                x, y = center
                if not isinstance(x, int) or not isinstance(y, int):
                    raise ParametersError(
                        "Setting failed, center coordinate need to be "
                        f"integer ({center})")
                if x < 0 or x > img.w or y < 0 or y > img.h:
                    raise ParametersError(
                        f"Pixel position outside image range, x:{x}, y: {y}")
                pos = (y * img.sl) + (x * (img.bpp // 8))  # Color is 8 bits
            else:
                raise ParametersError(f"Invalid center format {center}. "
                                      "Allowed (x, y)")
        else:
            raise ParametersError(f"Error: Invalid center instance {center}. "
                                  "Allowed instances are int/tuple")

        try:
            if img.data is not None:
                img.data[pos: pos + 4] = (color).to_bytes(4, 'little')
        except Exception as e:
            raise OperationError(f"Unable to set pixel: {e}")


class Stages(Protocol):
    def process(self, mlx: MlxVar, img: ImgData,
                factor: float = 1.0, font_color=0xFFFFFFFF,
                bg_color=0x00000000) -> ImgData:
        pass


class ImageScaler:
    def process(self, mlx: MlxVar, img: ImgData,
                factor: float = 1.0, font_color=0xFFFFFFFF,
                bg_color=0x00000000) -> ImgData:
        if factor <= 0:
            raise ParametersError(
                "Image scaling failed, Factor has to be "
                f"bigger than 0, not {factor}")
        try:
            new_img = ImageOperations.generate_blank_image(
                mlx, int(img.w * factor), int(img.h * factor))
        except ImgError as e:
            raise ImgError(f"{type(e).__name__}: {e}")

        for y in range(new_img.h):
            for x in range(new_img.w):
                new_img_pos = y * new_img.sl + (4 * x)
                img_pos = int(y / factor) * img.sl + \
                    (4 * int(x / factor))
                if new_img.data is not None and img.data is not None:
                    new_img.data[new_img_pos: new_img_pos + 4] = \
                        img.data[img_pos: img_pos + 4]
                else:
                    raise OperationError(
                        "Cropping failed, The dest or src image is empty"
                        )
        return new_img


class TxtColorChanger:
    def process(self, mlx: MlxVar, img: ImgData,
                factor: float = 1.0, font_color=0xFFFFFFFF,
                bg_color=0x00000000) -> ImgData:
        try:
            new_img = ImageOperations.generate_blank_image(mlx, img.w, img.h)
        except ImgError as e:
            raise ImgError(f"{type(e).__name__}: {e}")

        try:
            for i in range(0, new_img.h * new_img.w * 4, 4):
                if img.data is not None and new_img.data is not None:
                    if img.data[i + 1] == 0 and img.data[i + 2] == 0 and \
                            img.data[i + 3] == 0:
                        new_img.data[i: i + 4] = \
                            (bg_color).to_bytes(4, "little")
                    else:
                        new_img.data[i: i + 4] = (font_color).to_bytes(
                            4, "little")
            return new_img
        except Exception as e:
            raise OperationError(
                f"Unable to change letter colour: {e}"
            )


class TxtToImage:
    def __init__(self, base_letter_map: Dict[str, ImgData],
                 extended_letter_dict: Dict[str, ImgData]) -> None:
        self.stages: List[Stages] = []
        self.base_letter_map = base_letter_map
        self.extended_letter_map: Dict[str, ImgData] = {}

    def add_stages(self, stage: Stages):
        self.stages.append(stage)

    def print_txt(self, mlx: MlxVar, buff_img: ImgData, txt: str,
                  origin: Tuple, factor: float = 1.0, font_color=0xFFFFFFFF,
                  bg_color=0x00000000) -> int:
        x, y = origin
        for letter in txt:
            try:
                comb_key = f"{letter}_{factor}_{font_color}_{bg_color}"
                img = self.extended_letter_map.get(comb_key)
                if img is None:
                    try:
                        img = self.base_letter_map[letter]
                    except KeyError:
                        img = self.base_letter_map[" "]
                    for stage in self.stages:
                        img = stage.process(mlx, img, factor, font_color,
                                            bg_color)
                    if img is not None:
                        self.extended_letter_map[comb_key] = img
                ImageOperations.copy_img(buff_img, img, (x, y))
                x += img.w
            except Exception as e:
                raise OperationError(
                    f"Unable to print '{letter}'-> {type(e).__name__}: {e}"
                )
        return x


def tester():
    from srcs.mlx_tools.LetterToImageMapper import LetterToImageMapper
    from srcs.mlx_tools.BaseMLX import MyMLX
    try:
        mlx = MyMLX(1000, 800)
        # image = "images/alphabets.xpm"
        letter_map = LetterToImageMapper(mlx.mlx)
        # copy_img_to_buffer(mlx.mlx.buff_img, mlx.mlx.letter_img, (0, 0))
        letter_map.create_map()
        ImageOperations.copy_img(
            mlx.mlx.buff_img, mlx.mlx.base_letter_map["A"], (0, 0))
        ImageOperations.copy_img(
            mlx.mlx.buff_img, mlx.mlx.base_letter_map["e"], (50, 0))
        ImageOperations.copy_img(
            mlx.mlx.buff_img, mlx.mlx.base_letter_map["1"], (150, 0))
        ImageOperations.copy_img(
            mlx.mlx.buff_img, mlx.mlx.base_letter_map["("], (100, 0))
        ImageOperations.copy_img(
            mlx.mlx.buff_img, mlx.mlx.base_letter_map[")"], (200, 0))
        scaler = ImageScaler()
        scaled_a = scaler.process(mlx.mlx, mlx.mlx.base_letter_map["A"], 0.5)
        ImageOperations.copy_img(mlx.mlx.buff_img, scaled_a, (250, 0))

        letter_color = TxtColorChanger()
        colored_a = letter_color.process(mlx.mlx, mlx.mlx.base_letter_map["A"])

        txt_to_img = TxtToImage(mlx.mlx.base_letter_map,
                                mlx.mlx.extended_letter_map)
        txt_to_img.add_stages(scaler)
        txt_to_img.add_stages(letter_color)
        txt_to_img.print_txt(mlx.mlx, mlx.mlx.buff_img,
                             "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                             (0, 180), 0.5)
        txt_to_img.print_txt(mlx.mlx, mlx.mlx.buff_img,
                             "abcdefghijklmnopqrstuvwxyz",
                             (0, 260))
        txt_to_img.print_txt(mlx.mlx, mlx.mlx.buff_img,
                             "0123456789",
                             (0, 340))
        txt_to_img.print_txt(mlx.mlx, mlx.mlx.buff_img,
                             ".,;:_#'!\"/?<>%&*()",
                             (0, 420))

        ImageOperations.copy_img(mlx.mlx.buff_img, colored_a, (300, 0))

        mlx.mlx.mlx.mlx_put_image_to_window(
            mlx.mlx.mlx_ptr, mlx.mlx.win_ptr, mlx.mlx.buff_img.img, 0, 0)
        mlx.start_mlx()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    tester()
