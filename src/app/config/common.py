from pathlib import Path
from typing import Final

from litestar.utils.module_loader import module_to_os_path

DEFAULT_MODULE_NAME = "src.app"

TRUE_VALUES = {"True", "true", "1", "yes", "Y", "T"}
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)
