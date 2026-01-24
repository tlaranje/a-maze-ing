from ctypes import c_void_p, c_uint
from typing import Protocol, Any, Callable


class MLX(Protocol):
    def mlx_init(self) -> c_void_p: ...
    ...

    def mlx_new_image(
            self, mlx_ptr: c_void_p, width: c_uint, height: c_uint
    ) -> c_void_p: ...

    def mlx_get_data_addr(
            self, img_ptr: Any
    ) -> tuple[bytearray, int, int, int]: ...

    def mlx_new_window(
            self, mlx_ptr: c_void_p, width: c_uint, height: c_uint, title: str
    ) -> c_void_p: ...

    def mlx_destroy_window(
            self, mlx_ptr: c_void_p, win_ptr: c_void_p
    ) -> int: ...

    def mlx_key_hook(
            self, win_ptr: c_void_p, func: Callable[..., Any], param: Any
    ) -> int: ...

    def mlx_hook(
            self, win_ptr: c_void_p, event: int, mask: int,
            func: Callable[..., Any], param: Any
    ) -> int: ...

    def mlx_loop_hook(
            self, mlx_ptr: c_void_p, func: Callable[..., Any], param: Any
    ) -> int: ...

    def mlx_loop(
            self, mlx_ptr: c_void_p
    ) -> int: ...

    def mlx_put_image_to_window(
            self, mlx_ptr: c_void_p, win_ptr: c_void_p,
            img_ptr: c_void_p, x: int, y: int
    ) -> int: ...

    def mlx_loop_exit(self, mlx_ptr: c_void_p) -> int: ...

    def mlx_release(self, mlx_ptr: c_void_p) -> int: ...
