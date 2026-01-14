import sys


class ConfigData:
    def __init__(self) -> None:
        self.width: int = None
        self.height: int = 0
        self.entry: tuple = {0, 0}
        self.exit: tuple = {0, 0}
        self.output_file: str = ""
        self.perfect: bool = None


def read_config_file(file: str) -> ConfigData:
    config_data = ConfigData()
    try:
        with open(file, "r") as fd:
            for line in fd:
                key = line.split("=")[0]
                value = line.split("=")[1]
                match key:
                    case "WIDTH":
                        config_data.width = int(value)
                    case "HEIGHT":
                        config_data.height = int(value)
                    case "ENTRY":
                        config_data.entry = tuple(map(int, value.split(",")))
                    case "EXIT":
                        config_data.exit = tuple(map(int, value.split(",")))
                    case "OUTPUT_FILE":
                        config_data.output_file = value
                    case "PERFECT":
                        config_data.perfect = value
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return config_data
