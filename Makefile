# === Main script ===
MAIN        := a_maze_ing.py

# === Commands ===
P3          := python3
RM          := rm -rf
FIND        := find
CC          := gcc

# === Sources ===
LIBXCB	    := $(HOME)/.brew/lib/libxcb.a
LIBMLX	    := libs/libmlx.so

# === Flags (via pkg-config) ===
PKG := pkg-config
CFLAGS  := $(PKG) --cflags xcb xcb-keysyms vulkan zlib libbsd
LDFLAGS := $(PKG) --libs   xcb xcb-keysyms vulkan zlib libbsd


# === Build targets ===
install: $(LIBXCB) $(LIBMLX)
	$(P3) -m pip install --upgrade pip
	$(P3) -m pip install flake8
	$(P3) -m pip install mypy

$(LIBXCB):
	brew update
	brew install libxcb

$(LIBMLX):
	make -C libs
	cp -r libs/python/src/mlx mazegen
	cp $(LIBMLX) mazegen/mlx

run:
	@$(P3) $(MAIN) config.txt

debug:
	@$(P3) -m pdb $(MAIN) config.txt

clean:
	@$(FIND) . -type d -name "__pycache__" -exec $(RM) {} +
	@$(FIND) . -type d -name ".mypy_cache" -exec $(RM) {} +
	@$(FIND) . -type d -name ".pytest_cache" -exec $(RM) {} +
	@$(FIND) . -type f -name "*.pyc" -delete
	@$(FIND) . -type f -name "*.pyo" -delete
	@$(RM) $(BIN)
	@$(RM) $(LIBMLX)

# Lint
lint:
	@flake8 .
	@mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# Lint strict
lint-strict:
	@flake8 .
	@mypy . --strict

.PHONY: install run debug clean lint lint-strict c-run
