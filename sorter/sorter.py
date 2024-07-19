from dataclasses import field, dataclass
from pathlib import Path
from typing import Iterable

from core.file import ExpressionFile


@dataclass
class Sorter:
    source: Iterable[ExpressionFile]
    target_dir: Path
    genes: dict[str, Path] = field(default_factory=dict)

    def sort(self):
        if not self.target_dir.exists():
            self.target_dir.mkdir(parents=True, exist_ok=True)
        for item in self.target_dir.iterdir():
            if item.is_file():
                item.unlink()
        i: int = 0
        for source in self.source:
            i += 1
            if i % 100 == 0:
                print(i, " sources analyzed.")
            for line in source.rows():
                gene = line[0]
                expression_1 = line[1]
                expression_2 = line[2]
                if gene not in self.genes:
                    target = self.target_dir / (gene + '.txt')
                    open(target, 'w')
                    self.genes[gene] = target
                with open(self.genes[gene], 'a') as file:
                    file.write(source.path.name.split(".")[0] + "," + expression_1 + ","
                               + expression_2 + ";\n")

