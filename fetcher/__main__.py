from pathlib import Path

from fetcher import Fetcher

if "__main__" == __name__:
    source_dir_path: str = "data/GSE120584_RAW"
    target_file_path: str = "data/table.txt"

    main_dir = Path.cwd().parent
    Fetcher(main_dir / source_dir_path, main_dir / target_file_path, overwrite=False).fetch()
