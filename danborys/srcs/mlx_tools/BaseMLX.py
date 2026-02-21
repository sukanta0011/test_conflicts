from typing import Dict, Tuple
from mlx import Mlx
from srcs.mlx_tools.mlx_errors import MLXError
from srcs.mlx_tools.ImageOperations import ImgData, ImageOperations


class MlxVar:
    def __init__(self) -> None:
        self.mlx = None
        self.mlx_ptr = None
        self.win_ptr = None
        self.screen_w = 0
        self.screen_h = 0
        self.buff_img = ImgData()
        self.static_bg = ImgData()


class MlxVarWithLetters(MlxVar):
    def __init__(self) -> None:
        super().__init__()
        self.letter_img = ImgData()
        self.base_letter_map: Dict[str, ImgData] = {}
        self.extended_letter_map: Dict[str, ImgData] = {}


class MyMLX:
    def __init__(self, name: str, w: int, h: int):
        self.name = name
        self.w = w
        self.h = h
        self.mlx = MlxVarWithLetters()
        self.init_mlx()

    def init_mlx(self):
        try:
            self.mlx.mlx = Mlx()
            self.mlx.mlx_ptr = self.mlx.mlx.mlx_init()
            self.mlx.win_ptr = self.mlx.mlx.mlx_new_window(
                self.mlx.mlx_ptr, self.w, self.h, self.name)
            self.mlx.buff_img = ImageOperations.generate_blank_image(
                self.mlx, self.w, self.h)
            self.mlx.static_bg = ImageOperations.generate_blank_image(
                self.mlx, self.w, self.h)
            self.set_background(self.mlx.static_bg, (0, 0), self.w, self.h)
            # print(f"Buffer image: {self.mlx.mlx.mlx_get_data_addr(
            # self.mlx.buff_img.img)}")
            self.mlx.mlx.mlx_clear_window(self.mlx.mlx_ptr, self.mlx.win_ptr)
            self.mlx.mlx.mlx_mouse_hook(self.mlx.win_ptr,
                                        self.mymouse, self.mlx)
            self.mlx.mlx.mlx_key_hook(self.mlx.win_ptr, self.mykey, self.mlx)
            self.mlx.mlx.mlx_hook(self.mlx.win_ptr, 33, 0,
                                  self.stop_mlx, self.mlx)
        except Exception as e:
            raise MLXError(
                f"Mlx initialization failed. {type(e).__name__}: {e}")

    def get_mlx(self) -> MlxVar:
        return self.mlx

    def start_mlx(self):
        self.mlx.mlx.mlx_loop(self.mlx.mlx_ptr)

    def stop_mlx(self, mlx_var):
        self.mlx.mlx.mlx_loop_exit(self.mlx.mlx_ptr)
        self.clean_mlx()

    def clean_mlx(self):
        self.mlx.mlx.mlx_destroy_image(self.mlx.mlx_ptr,
                                       self.mlx.buff_img.img)
        self.mlx.mlx.mlx_destroy_image(self.mlx.mlx_ptr,
                                       self.mlx.static_bg.img)
        if self.mlx.letter_img.img is not None:
            self.mlx.mlx.mlx_destroy_image(self.mlx.mlx_ptr,
                                           self.mlx.letter_img.img)
        if len(self.mlx.base_letter_map) > 0:
            for _, val in self.mlx.base_letter_map.items():
                self.mlx.mlx.mlx_destroy_image(self.mlx.mlx_ptr, val.img)
        if len(self.mlx.base_letter_map) > 0:
            for _, val in self.mlx.extended_letter_map.items():
                self.mlx.mlx.mlx_destroy_image(self.mlx.mlx_ptr, val.img)
        self.mlx.mlx.mlx_destroy_window(self.mlx.mlx_ptr, self.mlx.win_ptr)

    def mymouse(self, button, x, y, mystuff):
        print(f"Got mouse event! button {button} at {x},{y}.")

    def mykey(self, key_num, mlx_var):
        pass
        # print(f"Got key {keynum}, and got my stuff back:")
        # if keynum == 112:
        #     print("Next Move")

    def put_buffer_image(self):
        if self.mlx.buff_img is not None:
            self.mlx.mlx.mlx_put_image_to_window(
                self.mlx.mlx_ptr, self.mlx.win_ptr, self.mlx.buff_img.img,
                0, 0)
        else:
            print("Error: buffer image is not set")

    def set_background(self, img: ImgData, center: Tuple,
                       w: int, h: int, color=0xFF000000):
        if w > img.w:
            w = img.w
        if h > img.h:
            h = img.h
        xc, yc = center
        pixel_bytes = color.to_bytes(4, 'little')
        for y in range(yc, yc + h):
            start = y * img.sl + 4 * xc
            end = start + 4 * w
            if img.data is not None:
                img.data[start:end] = pixel_bytes * w

    def rgb_to_hex(self, r: int = 0, g: int = 0, b: int = 0):
        return 0xFF000000 | r << 16 | g << 8 | b
