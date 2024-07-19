import re

import requests

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable

EXPLORED: set


class Sex(Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass
class TableRow:
    id: str
    sex: Sex
    age: int
    diagnosis: str
    apoe4: int | None


@dataclass
class Fetcher:
    source_dir: Path
    target_file: Path
    overwrite: bool = True
    pattern: str = r'\b(diagnosis|Diagnosis|age|Age|sex|Sex|apoe4|Apoe4):\s*([^<]+)'
    base_link: str = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi"
    param_key: str = "acc"

    def fetch(self) -> None:
        if self.overwrite:
            self._prepare_target()
        source_names: Iterable[str] = self._fetch_source_names()
        source_names = [s.split('_', 1)[0] for s in source_names]
        rows = self._fetch_data(source_names)
        self._save_data(rows)

    def _prepare_target(self) -> None:
        if self.target_file.exists():
            self.target_file.unlink()

        with self.target_file.open('w') as file:
            file.write("Sample,Age,Sex,Diagnosis,APOE4;\n")

    def _fetch_source_names(self) -> Iterable[str]:
        for source_file in self.source_dir.iterdir():
            yield source_file.name

    def _fetch_data(self, ids: Iterable[str]) -> Iterable[TableRow]:
        count: int = 0
        explored: set[str] = set()
        if not self.overwrite:
            with self.target_file.open() as file:
                for line in file:
                    explored.add(line.split(',', 1)[0])
        for identifier in ids:
            if not self.overwrite:
                if identifier in explored:
                    continue
            response = requests.get(self.base_link, {self.param_key: identifier})
            response.raise_for_status()
            data = response.text
            start_index = data.find("<td nowrap>Characteristics</td>") + 32
            if start_index != 31:
                last_index = data.find('</tr>', start_index)
                if last_index != -1:
                    middle = data[start_index:last_index]
                    matches = re.findall(self.pattern, middle)
                    result = {key.lower(): value.strip() for key, value in matches}
                    yield TableRow(
                        id=identifier,
                        sex=Sex.MALE if str(result["sex"]).lower() == "male" else Sex.FEMALE,
                        age=int(result["age"]),
                        diagnosis=str(result["diagnosis"]),
                        apoe4=int(result["apoe4"]) or None
                    )
            count += 1
            if count % 100 == 0:
                print(str(count) + " samples fetched.")

    def _save_data(self, rows: Iterable[TableRow]) -> None:
        with self.target_file.open('a') as file:
            for row in rows:
                file.write(row.id + "," + str(row.age) + "," + row.sex.value + ","
                           + row.diagnosis + "," + str(row.apoe4) + ";\n")

