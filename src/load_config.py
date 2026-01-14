import sys
from typing import Optional


class ConfigData:
    """All program required parameters"""

    def __init__(self) -> None:
        self.width: int = None
        self.height: int = None
        self.entry: tuple = None
        self.exit: tuple = None
        self.output_file: str = None
        self.perfect: bool = None


def uint(string: str, only_positive: Optional[bool] = False) -> int:
    """Convert a string to an unsigned integer"""
    number: int = int(string)
    if only_positive and number <= 0:
        raise ValueError("Number must be positive")
    if number < 0:
        raise ValueError("Number must be unsigned")
    return number


def parse_config_data(config: ConfigData, key: str, value: str) -> None:
    """Get all mandatory config datas and raise errors"""
    match key:
        case "WIDTH":
            config.width = uint(value, only_positive=True)
        case "HEIGHT":
            config.height = uint(value, only_positive=True)
        case "ENTRY":
            entry: tuple = tuple(map(uint, value.split(",")))
            if len(entry) != 2:
                raise Exception("ENTRY must be x, y values")
            config.entry = entry
        case "EXIT":
            exit_: tuple = tuple(map(uint, value.split(",")))
            if len(exit_) != 2:
                raise Exception("EXIT must be x, y values")
            config.exit = exit_
        case "OUTPUT_FILE":
            config.output_file = value
        case "PERFECT":
            if value != "True" and value != "False":
                raise Exception("PERFECT must be True or False")
            config.perfect = value == "True"


def read_config_file(file: str) -> ConfigData:
    """Read and parse the configuration file"""
    config_data: ConfigData = ConfigData()
    try:
        with open(file, "r") as fd:
            for line in fd:
                key, value = line.split("=")
                parse_config_data(config_data, key.strip(), value.strip())
        for _, value in vars(config_data).items():
            if value is None:
                raise ValueError("Missing mandatory values on config")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    return config_data
