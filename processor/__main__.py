from pathlib import Path

from processor import Processor

if "__main__" == __name__:
    source_dir_path: str = "data/GSE120584_RAW"
    target_dir_path: str = "data/GSE120584_PROCESSED"

    main_dir = Path.cwd().parent
    Processor(main_dir / source_dir_path, main_dir / target_dir_path, overwrite=True).process()
