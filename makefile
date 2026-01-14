# === Main script ===
MAIN        := src/a_maze_ing.py

# === Commands ===
P3          := python3
RM          := rm -rf
FIND        := find
CC          := gcc

# === Sources ===
SRC         := src/main.c
BIN         := a_maze_ing

# === Flags (via pkg-config) ===
PKG := pkg-config
CFLAGS  := $(PKG) --cflags xcb xcb-keysyms vulkan zlib libbsd
LDFLAGS := $(PKG) --libs   xcb xcb-keysyms vulkan zlib libbsd


# === Build targets ===
install:
	$(P3) -m pip install --upgrade pip
	$(P3) -m pip install flake8
	$(P3) -m pip install mypy

run:
	@$(P3) $(MAIN)

debug:
	@$(P3) -m pdb $(MAIN)

clean:
	@$(FIND) . -type d -name "__pycache__" -exec $(RM) {} +
	@$(FIND) . -type d -name ".mypy_cache" -exec $(RM) {} +
	@$(FIND) . -type d -name ".pytest_cache" -exec $(RM) {} +
	@$(FIND) . -type f -name "*.pyc" -delete
	@$(FIND) . -type f -name "*.pyo" -delete
	@$(RM) $(BIN)

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

# === C build ===
$(BIN): $(SRC)
	$(CC) $(SRC) -o $(BIN) $(CFLAGS) $(LDFLAGS)

c-run: $(BIN)
	./$(BIN)

.PHONY: install run debug clean lint lint-strict c-run
