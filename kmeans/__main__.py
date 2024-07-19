from pathlib import Path

from kmeans import Manager

if "__main__" == __name__:
    files_dir_path: str = "data/GSE120584_SORTED"
    destination_dir_path: str = "data/GSE120584_RESULTS_3"
    table_file_path: str = "data/table.txt"

    main_dir = Path.cwd().parent

    Manager(main_dir / table_file_path, main_dir / files_dir_path,
            main_dir / destination_dir_path).run()
