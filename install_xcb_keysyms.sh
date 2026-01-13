#!/bin/sh

set -e

echo "=== Installing xcb-util-keysyms locally ==="

PREFIX="$HOME/local"
VERSION="0.4.1"
TARBALL="xcb-util-keysyms-$VERSION.tar.gz"
URL="https://xcb.freedesktop.org/dist/$TARBALL"
DIR="xcb-util-keysyms-$VERSION"

echo "→ Creating local prefix at $PREFIX"
mkdir -p "$PREFIX"

echo "→ Downloading $TARBALL"
wget -q "$URL"

echo "→ Extracting archive"
tar -xvf "$TARBALL"

echo "→ Entering directory $DIR"
cd "$DIR"

echo "→ Configuring with prefix=$PREFIX"
./configure --prefix="$PREFIX"

echo "→ Building"
make

echo "→ Installing"
make install

echo "→ Verifying installation"

echo "   - Checking header:"
if [ -f "$PREFIX/include/xcb/xcb_keysyms.h" ]; then
    echo "     ✓ xcb_keysyms.h found"
else
    echo "     ✗ xcb_keysyms.h NOT found"
fi

echo "   - Checking libraries:"
ls "$PREFIX/lib" | grep keysyms || echo "     ✗ No keysyms libraries found"

echo "=== Done ==="
