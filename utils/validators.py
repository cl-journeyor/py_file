from pathlib import Path
from typing import Literal, Tuple
from utils import consts

def safe_path(path: str) -> Tuple[Literal[False], str] | Tuple[Literal[True], Path]:
    parsed_path = Path(path)

    if parsed_path.is_absolute():
        return (False, 'Absolute paths are not allowed')

    target_path = (consts.FILES_DIR / parsed_path).resolve()

    if not target_path.is_relative_to(consts.FILES_DIR):
        return (False, 'Unauthorized path')

    return (True, target_path)
