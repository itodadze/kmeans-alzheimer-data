from pathlib import Path

from core.file import ExpressionFile
from sorter import Sorter

if "__main__" == __name__:
    source_dir_path: str = "data/GSE120584_PROCESSED"
    target_dir_path: str = "data/GSE120584_SORTED"

    main_dir = Path.cwd().parent
    Sorter([ExpressionFile(source) for source in (main_dir / source_dir_path).iterdir()],
           main_dir / target_dir_path).sort()
