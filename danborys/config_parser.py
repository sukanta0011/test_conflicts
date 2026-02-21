from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Dict, Tuple, Self, List
from pathlib import Path
import sys


class Configuration(BaseModel):
    width: int = Field(ge=1, le=2147483648)
    height: int = Field(ge=1, le=2147483648)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str = Field(min_length=5)
    perfect: bool

    @model_validator(mode="before")
    def create_tuples(cls, row_data: Dict) -> Dict:
        entry_x_y = row_data.get("entry")
        if not entry_x_y:
            raise ValueError(" - Field 'ENTRY': No value")
        entry_x_y = entry_x_y.split(",")
        exit_x_y = row_data.get("exit")
        if not exit_x_y:
            raise ValueError(" - Field 'EXIT': No value")
        exit_x_y = exit_x_y.split(",")
        row_data["entry"] = tuple(entry_x_y)
        row_data["exit"] = tuple(exit_x_y)
        return row_data

    @model_validator(mode="after")
    def check_config(self) -> Self:
        if self.entry == self.exit:
            raise ValueError(" - Field 'ENTRY': must be different from 'EXIT'")
        if self.entry[0] < 0 or self.entry[1] < 0:
            raise ValueError(" - Field 'ENTRY': contains negative coordinates")
        if self.exit[0] < 0 or self.exit[1] < 0:
            raise ValueError("- Field 'EXIT': contains negative coordinates")
        if self.entry[0] >= self.width:
            raise ValueError(" - Field 'ENTRY': x coordinate bigger "
                             "than 'WIDTH'")
        if self.entry[1] >= self.height:
            raise ValueError(" - Field 'ENTRY': y coordinate bigger "
                             "than 'HEIGHT'")
        if self.exit[0] >= self.width:
            raise ValueError(" - Field 'EXIT': x coordinate bigger "
                             "than 'WIDTH'")
        if self.exit[1] >= self.height:
            raise ValueError(" - Field 'EXIT': y coordinate bigger "
                             "than 'HEIGHT'")
        if not self.output_file.endswith(".txt"):
            raise ValueError(" - Field 'OUTPUT': "
                             "file name must contain '.txt'")
        return self


class ConfigParser():
    @staticmethod
    def parse_config(file_path: Path) -> Configuration:
        row_data: Dict[str, str] = {}
        data: List[str]
        try:
            with open(file_path, mode="r") as f:
                data = f.readlines()
        except FileNotFoundError:
            print(f"File {file_path} not found", file=sys.stderr)
            exit(1)
        for line in data:
            if line.startswith("#"):
                continue
            if "=" not in line:
                print(f"Invalid configuration line: {line}", file=sys.stderr)
                exit(1)
            line = line.strip("\n").strip()
            key, value = line.split("=", 1)
            row_data[key.lower()] = value
        try:
            return Configuration(**row_data)
        except ValidationError as e:
            print("Configuration parsing error:", file=sys.stderr)
            for error in e.errors():
                loc = error["loc"]
                message = error["msg"].removeprefix("Value error, ")
                if loc:
                    field = loc[0].upper()
                    print(f" - Field '{field}': {message}", file=sys.stderr)
                else:
                    print(f"{message}", file=sys.stderr)
            exit(1)
