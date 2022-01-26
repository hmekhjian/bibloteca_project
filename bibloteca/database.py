"""This module provides the bibloteca database functionality."""

# bibloteca/database.py

import configparser
from pathlib import Path

from bibloteca import DB_WRITE_ERROR, SUCCESS


DEFAULT_DB_FILE_PATH = Path.home().joinpath("." + Path.home().stem + "_library.json")


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the library database."""
    try:
        db_path.write_text("[]")  # Empty entry
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
