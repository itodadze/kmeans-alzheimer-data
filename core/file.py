from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Any

from fetcher.fetcher import Sex

Row: type = list[Any]


@dataclass(frozen=True)
class File:
    path: Path

    def rows(self) -> Iterable[Row]:
        with self.path.open() as file:
            for line in file:
                yield line[:-2].split(',')

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, File):
            return other.path.name == self.path.name
        return False

    def __hash__(self) -> int:
        return hash(self.path.name)


@dataclass(frozen=True)
class ExpressionFile(File):
    def rows(self) -> Iterable[Row]:
        for row in super().rows():
            current = str(row[0])
            if current.startswith("Spike") or current.startswith("Negative") or current.startswith("No") or current.startswith("BLANK") or current.startswith("S-Probe") or current.startswith("QC-Probe"):
                continue
            else:
                yield row


@dataclass(frozen=True)
class SampleData:
    id: str
    age: int
    sex: Sex
    diagnosis: str
    apoe4: int


@dataclass(frozen=True)
class Table:
    file: File

    def as_dict(self) -> dict[str, SampleData]:
        result: dict[str, SampleData] = {}
        for row in self.file.rows():
            id = str(row[0])
            if id != "Sample":
                age = int(row[1])
                if str(row[2]) == "male":
                    sex = Sex.MALE
                else:
                    sex = Sex.FEMALE
                diagnosis = str(row[3]).lower()
                if str(row[4]) == "None":
                    apoe4 = 0
                else:
                    apoe4 = int(row[4])
                result[id] = SampleData(
                    id,
                    age,
                    sex,
                    diagnosis,
                    apoe4
                )
        return result

