from typing import Tuple
from srcs.mlx_tools.BaseMLX import MlxVar
from srcs.mlx_tools.mlx_errors import (
    ParametersError, ImgError
)
from srcs.mlx_tools.ImageOperations import ImageOperations, ImgData


class ShapeGenerator:
    @staticmethod
    def draw_line(mlx_var: MlxVar, img: ImgData, coordinate: Tuple,
                  len: int, direction: str = "v",
                  color=0xFFFFFFFF, thickness: int = 1) -> None:
        x, y = coordinate
        if not isinstance(x, int) or not isinstance(y, int):
            raise ParametersError(
                "Drawing line failed, center coordinate need to be "
                f"integer ({coordinate})")
        if direction == "h":
            if x < 0 or x + len > img.w:
                raise ParametersError(
                    "Drawing line failed. x coordinate out of range, "
                    f"({x}, {x + len})")
            if y - thickness // 2 > 0:
                y -= thickness // 2
            for i in range(thickness):
                for j in range(x, x + len):
                    ImageOperations.set_pixel(img, (j, y + i), color)
        elif direction == "v":
            if y < 0 or y + len > img.h:
                raise ParametersError(
                    "Drawing line failed. xy coordinate out of range, "
                    f"({y}, {y + len})")
            if x - thickness // 2 > 0:
                x -= thickness // 2
            for i in range(thickness):
                for j in range(y, y + len):
                    ImageOperations.set_pixel(img, (x + i, j), color)
        else:
            raise ParametersError(f"Drawing line failed. Unknown direction: "
                  f"{direction}. Allowed directions are 'v' and 'h'")

    @staticmethod
    def draw_hollow_square(mlx_var: MlxVar, img: ImgData, center: Tuple,
                           len: int, color=0xFFFFFFFF):
        try:
            x, y = center
            if not isinstance(x, int) or not isinstance(y, int):
                raise ParametersError(
                    "Drawing hollow square failed. center coordinate need to be "
                    f"integer ({center})")
            ShapeGenerator.draw_line(mlx_var, img, (x - len // 2, y + len // 2), len, "h", color)
            ShapeGenerator.draw_line(mlx_var, img, (x - len // 2, y - len // 2), len, "h", color)
            ShapeGenerator.draw_line(mlx_var, img, (x + len // 2, y - len // 2), len, "v", color)
            ShapeGenerator.draw_line(mlx_var, img, (x - len // 2, y - len // 2), len, "v", color)
        except Exception as e:
            raise ImgError(f"Drawing hollow square failed.-> {e}")
    
    @staticmethod
    def draw_filled_rectangle(mlx_var: MlxVar, img: ImgData, center: Tuple,
                              h: int, w: int, color=0xFFFFFFFF):
        try:
            x, y = center
            if not isinstance(x, int) or not isinstance(y, int):
                raise ParametersError(
                    "Drawing filled rectangle failed. center coordinate "
                    f"need to be integer ({center})")
            for i in range(y, y + h):
                ShapeGenerator.draw_line(mlx_var, img, (x, i), w, "h", color)
        except Exception as e:
            raise ImgError(f"Drawing filled rectangle failed.-> {e}")
