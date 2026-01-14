
def read_config_file(file: str) -> None:
    with open(file, "r") as fd:
        data = fd.read()
    print(data)
    