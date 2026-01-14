def create_window(xvar, title: str, width: int, height: int) -> None:
    # mlx_ptr, width, height, title
    win = xvar.mlx.mlx_new_window(
        xvar.mlx_ptr,
        width,
        height,
        title)

    if not win:
            raise Exception("Can't create window")

    xvar.windows.append(win)


def close_windows(xvar) -> None:
    def close_single_window(xvar, win):
        xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, win)
        xvar.windows.remove(win)

        if not xvar.windows:
            xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)

    for window in xvar.windows:
        # win_ptr, x_event, x_mask, callback, param
        xvar.mlx.mlx_hook(
            window,
            33,
            0,
            lambda w: close_single_window(xvar, w),
            window
        )
