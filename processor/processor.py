from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Processor:
    source_dir: Path
    target_dir: Path
    overwrite: bool = False

    def process(self) -> None:
        if not self.target_dir.exists():
            self.target_dir.mkdir(parents=True, exist_ok=True)
        if self.overwrite:
            for item in self.target_dir.iterdir():
                if item.is_file():
                    item.unlink()
        sources = self._fetch_sources()
        sources = [(s.split('_', 1)[0], p) for s, p in sources]
        self._load_data(sources)

    def _fetch_sources(self) -> Iterable[tuple[str, Path]]:
        for source_file in self.source_dir.iterdir():
            yield source_file.name, source_file

    def _load_data(self, sources: Iterable[tuple[str, Path]]) -> None:
        count: int = 0
        explored: set[str] = set()
        if not self.overwrite:
            for data_file in self.target_dir.iterdir():
                explored.add(data_file.name.split('.')[0])
        for source in sources:
            if source[0] not in explored:
                self._process(source[0], source[1])
                count += 1
                if count % 100 == 0:
                    print(str(count) + " data files processed.")

    def _process(self, name: str, source: Path) -> None:
        target = self.target_dir / (name + '.txt')
        with open(target, 'w') as t_f:
            with source.open() as s_f:
                counter = 0
                for line in s_f:
                    counter += 1
                    if counter < 9:
                        continue
                    split_line = line.split()
                    if split_line[4] == "No":
                        t_f.write(split_line[4] + " " + split_line[5] + "," + str(split_line[8]
                                                                                  + "," + str(split_line[10]) + ";\n"))
                    elif split_line[4] == "Negative" or split_line[4] == "Spike":
                        t_f.write(split_line[4] + " " + split_line[5] + " " + split_line[6] + "," + str(split_line[10]
                                                                                  + "," + str(split_line[12]) + ";\n"))
                    elif split_line[4][0] == "\"":
                        genes = [split_line[4][1:-1]]
                        i: int = 4
                        while True:
                            i += 1
                            genes.append(split_line[i][:-1])
                            if split_line[i][-1] == "\"":
                                break
                        for gene in genes:
                            t_f.write(gene + "," + split_line[2 * i - 2] + "," + split_line[2 * i] + ";\n")
                    else:
                        t_f.write(split_line[4] + "," + str(split_line[6]
                                                            + "," + str(split_line[8]) + ";\n"))
