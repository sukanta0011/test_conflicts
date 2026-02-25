from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Dict, Tuple, Self, List
from pathlib import Path
import sys


class Configuration(BaseModel):
    """
    Represents and validates the maze configuration parameters.

    This model defines all required configuration fields for maze generation
    and ensures their correctness using Pydantic validation.

    Attributes:
        width (int): Width of the maze grid. Must be >= 1.
        height (int): Height of the maze grid. Must be >= 1.
        entry (Tuple[int, int]): Entry cell coordinates (row, column).
        exit (Tuple[int, int]): Exit cell coordinates (row, column).
        output_file (str): Name of the output file where the maze
            representation will be saved. Must end with '.txt'.
        perfect (bool): Indicates whether the maze must be perfect
            (i.e., with a unique solution).
        seed (None | str): Optional seed used to make maze generation
            reproducible.
    """

    width: int = Field(ge=1, le=2147483648)
    height: int = Field(ge=1, le=2147483648)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str = Field(min_length=5)
    perfect: bool
    seed: None | str = Field(default=None)

    @model_validator(mode="before")
    def preprocess_fields(cls, row_data: Dict) -> Dict:
        """
        Preprocess and validate raw configuration values before model
        validation.

        This validator performs early transformations and strict checks:
            - Converts 'entry' and 'exit' from comma-separated strings
          (e.g., "0,1") into integer tuples (0, 1).
            - Ensures 'entry' and 'exit' contain exactly two integer values.
            - Enforces strict boolean parsing for the 'perfect' field,
          allowing only "true" or "false" (case-insensitive).
            - Converts the 'perfect' field into a boolean.

        Args:
            row_data (Dict): Raw configuration dictionary parsed
                from the configuration file.

        Returns:
            Dict: Updated dictionary with transformed values.

        Raises:
            ValueError:
                - If 'ENTRY' or 'EXIT' is missing.
                - If coordinates are not valid integers.
                - If 'PERFECT' is missing.
                - If 'PERFECT' is not strictly "true" or "false".
        """
        # ---- ENTRY ----
        entry_value = row_data.get("entry")
        if not entry_value:
            raise ValueError(" - Field 'ENTRY': No value")

        entry_parts = entry_value.split(",")
        if len(entry_parts) != 2:
            raise ValueError(" - Field 'ENTRY': must contain two integers")

        try:
            row_data["entry"] = (
                int(entry_parts[0]),
                int(entry_parts[1]),
            )
        except ValueError:
            raise ValueError(
                " - Field 'ENTRY': coordinates must be integers"
            )

        # ---- EXIT ----
        exit_value = row_data.get("exit")
        if not exit_value:
            raise ValueError(" - Field 'EXIT': No value")

        exit_parts = exit_value.split(",")
        if len(exit_parts) != 2:
            raise ValueError(" - Field 'EXIT': must contain two integers")

        try:
            row_data["exit"] = (
                int(exit_parts[0]),
                int(exit_parts[1]),
            )
        except ValueError:
            raise ValueError(
                " - Field 'EXIT': coordinates must be integers"
            )

        # ---- PERFECT ----
        perfect_value = row_data.get("perfect")
        if perfect_value is None:
            raise ValueError(" - Field 'PERFECT': No value")

        if perfect_value.lower() not in {"true", "false"}:
            raise ValueError(
                " - Field 'PERFECT': must be 'true' or 'false'"
            )

        row_data["perfect"] = perfect_value.lower() == "true"
        return row_data

    @model_validator(mode="after")
    def check_config(self) -> Self:
        """
        Perform cross-field validation of configuration values.

        Ensures:
            - Entry and exit are different.
            - Coordinates are non-negative.
            - Coordinates are inside maze bounds.
            - Output file has a '.txt' extension.

        Returns:
            Self: Validated configuration instance.

        Raises:
            ValueError: If any configuration constraint is violated.
        """
        if self.entry == self.exit:
            raise ValueError(" - Field 'ENTRY': must be different from 'EXIT'")
        if self.entry[0] < 0 or self.entry[1] < 0:
            raise ValueError(" - Field 'ENTRY': contains negative coordinates")
        if self.exit[0] < 0 or self.exit[1] < 0:
            raise ValueError("- Field 'EXIT': contains negative coordinates")
        if self.entry[0] >= self.height:
            raise ValueError(" - Field 'ENTRY': row bigger "
                             "than 'HEIGHT'")
        if self.entry[1] >= self.width:
            raise ValueError(" - Field 'ENTRY': column bigger "
                             "than 'WIDTH'")
        if self.exit[0] >= self.height:
            raise ValueError(" - Field 'EXIT': row coordinate bigger "
                             "than 'HEIGHT'")
        if self.exit[1] >= self.width:
            raise ValueError(" - Field 'EXIT': column bigger "
                             "than 'WIDTH'")
        if not self.output_file.endswith(".txt"):
            raise ValueError(" - Field 'OUTPUT': "
                             "file name must contain '.txt'")
        return self


class ConfigParser():
    """
    Utility class responsible for parsing a configuration file
    and returning a validated Configuration object.
    """

    @staticmethod
    def parse_config(file_path: Path) -> Configuration:
        """
        Parse a configuration file and validate its contents.

        The configuration file must follow the format:
            One KEY=VALUE pair (key=value is allowed) per line.

        Comment lines must start with '#'.

        Args:
            file_path (Path): Path to the configuration file.

        Returns:
            Configuration: A validated configuration instance.

        Raises:
            SystemExit: If the file is missing or contains invalid data.
        """
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
            if "=" not in line or " =" in line or "= " in line:
                print(f"Invalid configuration line: {line}", file=sys.stderr)
                exit(1)
            line = line.strip("\n").strip()
            key, value = line.split("=", 1)
            if not key or not value:
                print(f"Invalid configuration line: {line}", file=sys.stderr)
                exit(1)
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
