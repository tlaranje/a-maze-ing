How to install xcb-util-keysyms locally.

1 - Create a local installation directory
    mkdir -p ~/local

2 - Download the official tarball
    wget https://xcb.freedesktop.org/dist/xcb-util-keysyms-0.4.1.tar.gz

3 - Extract the archive
    tar -xvf xcb-util-keysyms-0.4.1.tar.gz
    cd xcb-util-keysyms-0.4.1

4 - Configure the build to install into ~/local
    ./configure --prefix=$HOME/local

5 - Compile
    make

6 - Install into ~/local
    make install

7 - Verify installation
    Headers:
        ls ~/local/include/xcb/

        You should see:
            xcb_keysyms.h

    Libraries:
        ls ~/local/lib | grep keysyms

        You should see:
            libxcb-keysyms.so
            libxcb-keysyms.so.1
            libxcb-keysyms.a

8 - Fix the config rule in the MLX Makefile
    In MLX Makefile, replace the "config:" rule with:

    config: configure.sh
        CFLAGS="-I$(HOME)/local/include" \
        LDFLAGS="-L$(HOME)/local/lib" \
        ./configure.sh

    ⚠️ Use TAB before each line inside the rule.

9 - Rebuild MLX
    make clean
    make

10 - Verify that MLX actually compiled the XCB backend
    After rebuilding MLX, check whether the symbol mlx__xcb_init exists inside your freshly built libmlx.so:

    cd ~/Documents/a-maze-ing/mlx_CLXV
    nm -D libmlx.so | grep mlx__xcb_init

    You should see one matching line.
    Like is - 000000000000d4d0 T mlx__xcb_init

    If nothing appears, the XCB backend was not compiled or linked, and you must fix the Makefile.

11 - Ensure Python uses your libmlx.so (not the pip one)
    Python loads the library from:
        ~/.local/lib/python3.10/site-packages/mlx/

    Replace the pip-installed version with your compiled one:
        cp libmlx.so ~/.local/lib/python3.10/site-packages/mlx/

    Verify again:
        nm -D ~/.local/lib/python3.10/site-packages/mlx/libmlx.so | grep mlx__xcb_init

    If the symbol appears, Python will now load the correct backend.

12 - Run your project
    In your project directory
    p -m src.a_maze_ing

