import sys


class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


def create_png_image(xvar, img_name: str, window: int, x: int, y: int) -> None:
    result = xvar.mlx.mlx_png_file_to_image(xvar.mlx_ptr, img_name)

    if not result:
        raise Exception("Can't load PNG")

    img_ptr, width, height = result

    if not img_ptr:
        raise Exception("Can't create png")

    data, bpp, sl, iformat = xvar.mlx.mlx_get_data_addr(img_ptr)

    img_data = ImgData()
    img_data.img = img_ptr
    img_data.width = width
    img_data.height = height
    img_data.data = data
    img_data.bpp = bpp
    img_data.sl = sl
    img_data.iformat = iformat

    xvar.images.append(img_data)

    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, window, img_data.img, x, y)


def create_xpm_image(xvar, img_name: str, window: int, x: int, y: int) -> None:
    result = xvar.mlx.mlx_xpm_file_to_image(xvar.mlx_ptr, img_name)

    if not result:
        raise Exception("Can't load PNG")

    img_ptr, width, height = result

    if not img_ptr:
        raise Exception("Can't create png")

    data, bpp, sl, iformat = xvar.mlx.mlx_get_data_addr(img_ptr)

    img_data = ImgData()
    img_data.img = img_ptr
    img_data.width = width
    img_data.height = height
    img_data.data = data
    img_data.bpp = bpp
    img_data.sl = sl
    img_data.iformat = iformat

    xvar.images.append(img_data)

    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, window, img_data.img, x, y)
