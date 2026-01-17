from mlx import Mlx


class ImgData:
    """Structure for image data"""

    def __init__(self, mlx: Mlx, mlx_ptr, width: int, height: int):
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        self.width: int = width
        self.height: int = height
        self.data, self.bpp, self.sl, self.iformat = \
            mlx.mlx_get_data_addr(self.ptr)
        self.total_size: int = len(self.data) - 3


# def create_xpm_image(xvar, img_name: str) -> ImgData:
#     result = xvar.mlx.mlx_xpm_file_to_image(xvar.mlx_ptr, img_name)
# 
#     if not result:
#         raise Exception("Can't load PNG")
# 
#     img_ptr, width, height = result
# 
#     if not img_ptr:
#         raise Exception("Can't create png")
# 
#     data, bpp, sl, iformat = xvar.mlx.mlx_get_data_addr(img_ptr)
# 
#     img_data = ImgData()
#     img_data.img = img_ptr
#     img_data.width = width
#     img_data.height = height
#     img_data.data = data
#     img_data.bpp = bpp
#     img_data.sl = sl
#     img_data.iformat = iformat

#    return img_data

def draw_wall(buffer_img: ImgData, start_x: int, start_y: int, size: int, color: int) -> None:
    """Draw block of pixels on images buffer"""
    start_x *= size
    start_y *= size
    for _ in range(size):
        x: int = start_x
        for _ in range(size):
            pos: int = (buffer_img.width * start_y + x) * 4
            if pos >= buffer_img.total_size:
                continue
            buffer_img.data[pos:pos+4] = color.to_bytes(4, 'little')
            x += 1
        start_y += 1
