import random

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Any

from core.file import File, SampleData, Table
from fetcher.fetcher import Sex


class Statistics:
    total: int
    sex: dict[Sex, int]
    apoe4: dict[int, int]
    diagnosis: dict[str, int]
    age: dict[int, int]

    def __init__(self) -> None:
        self.total = 0
        self.sex = {
            Sex.MALE: 0,
            Sex.FEMALE: 0
        }
        self.apoe4 = {
            0: 0,
            1: 0,
            2: 0
        }
        self.diagnosis = {
            "ad": 0,
            "dlb": 0,
            "mci": 0,
            "nc": 0,
            "vad": 0
        }
        self.age = {}

    def avg_age(self) -> float:
        return sum([age * self.age[age] for age in self.age.keys()]) / sum(self.age.values())

    def as_dict(self) -> dict[str, Any]:
        return {
            "age": self.avg_age(),
            "sex": self.sex,
            "apoe4": self.apoe4,
            "diagnosis": self.diagnosis,
            "total": self.total
        }

    def proportions(self) -> dict[str, float]:
        return {
            "age": self.avg_age(),
            "male_ratio": float(self.sex[Sex.MALE]) / self.total,
            "apoe4_2": float(self.apoe4[2]) / self.total,
            "apoe4_1": float(self.apoe4[1]) / self.total,
            "ad": float(self.diagnosis["ad"]) / self.total,
            "dlb": float(self.diagnosis["dlb"]) / self.total,
            "mci": float(self.diagnosis["mci"]) / self.total,
            "nc": float(self.diagnosis["nc"]) / self.total,
            "vad": float(self.diagnosis["vad"]) / self.total
        }

    def distance_score(self, other: dict[str, float]) -> float:
        if self.total < 3:
            return 0
        score: float = 0.0
        proportions = self.proportions()
        score += abs(proportions["age"] - other["age"]) # approx 1 - 2 maybe
        score += (Statistics._proportion(proportions["male_ratio"], other["male_ratio"]) - 1) * 2
        score += (Statistics._proportion(proportions["apoe4_2"], other["apoe4_2"]) - 1) * 2
        score += (Statistics._proportion(proportions["apoe4_1"], other["apoe4_1"]) - 1) * 2
        score += (Statistics._proportion(proportions["ad"], other["ad"]) - 1) * 3
        score += (Statistics._proportion(proportions["dlb"], other["dlb"]) - 1) * 2
        score += (Statistics._proportion(proportions["mci"], other["mci"]) - 1) * 2
        score += (Statistics._proportion(proportions["nc"], other["nc"]) - 1) * 3
        score += (Statistics._proportion(proportions["vad"], other["vad"]) - 1) * 3
        if self.total < 6:
            return score / 6
        if self.total < 8:
            return score / 5
        if self.total < 10:
            return score / 4
        if self.total < 13:
            return score / 3
        if self.total < 16:
            return score / 2
        if self.total < 20:
            return score / 1.5
        return score

    @staticmethod
    def _proportion(a: float, b: float) -> float:
        if a < 0.02 and b < 0.02:
            return 1
        if b < 0.01:
            if (a - b) < 0.04:
                return 1
            else:
                return 20 * (a - b)
        if a < 0.01:
            if (b - a) < 0.04:
                return 1
            else:
                return 20 * (b - a)
        if a >= b:
            return a / b
        else:
            return b / a


@dataclass(frozen=True)
class SampleEntry:
    id: str
    expression: float


@dataclass
class Cluster:
    id: str
    center: float
    table: dict[str, SampleData]
    samples: Iterable[SampleEntry]

    def distance(self, sample: SampleEntry) -> float:
        return abs(sample.expression - self.center)

    def assign(self, samples: Iterable[SampleEntry]) -> int:
        count = len(set(samples).difference(self.samples))
        self.samples = samples
        return count

    def update(self) -> None:
        self.center = sum([sample.expression for sample in self.samples]) / len(list(self.samples))

    def statistics(self) -> Statistics:
        statistics = Statistics()
        for entry in self.samples:
            data = self.table[entry.id]
            statistics.total += 1
            statistics.sex[data.sex] += 1
            statistics.apoe4[data.apoe4] += 1
            statistics.diagnosis[data.diagnosis] += 1
            if data.age not in statistics.age.keys():
                statistics.age[data.age] = 0
            statistics.age[data.age] += 1
        return statistics


@dataclass
class KMeans:
    clusters: list[Cluster]
    samples: list[SampleEntry]
    _last_changes = -1
    _iteration = 0

    def run(self) -> None:
        self._last_changes = -1
        self._iteration = 0
        while self._last_changes != 0:
            self._run()

    def _run(self) -> None:
        self._iteration += 1
        self._last_changes = 0
        partitions: list[list[SampleEntry]] = []
        for _ in self.clusters:
            partitions.append([])
        j: int = 0
        for sample in self.samples:
            j += 1
            best_cluster: int = -1
            best_score: float = -1
            for i, cluster in enumerate(self.clusters):
                distance = cluster.distance(sample)
                if best_score == -1 or distance < best_score:
                    best_score = distance
                    best_cluster = i
            partitions[best_cluster].append(sample)
        for i, cluster in enumerate(self.clusters):
            self._last_changes += cluster.assign(partitions[i])
        for cluster in self.clusters:
            cluster.update()


@dataclass
class ClusterFactory:
    id: str
    table: dict[str, SampleData]
    entries: list[SampleEntry]

    def choose(self) -> Cluster:
        entry: SampleEntry = random.choice(self.entries)
        self.entries = list(self.entries)
        self.entries.remove(entry)
        return Cluster(self.id, entry.expression, self.table, [])


@dataclass
class Run:
    table: dict[str, SampleData]
    dir: Path
    gene: str
    k: int

    def run(self) -> list[Cluster]:
        entries = [SampleEntry(str(row[0]), float(row[1])) for row in
                   File(self.dir / (self.gene + ".txt")).rows()]
        factory = ClusterFactory(self.gene, self.table, entries)
        clusters = [factory.choose() for _ in range(self.k)]
        KMeans(clusters, entries).run()
        return clusters


@dataclass
class Manager:
    table_file: Path
    data_dir: Path
    destination_dir: Path
    cut_off_deviation_score: float = 31
    cluster_count = 3

    def run(self) -> None:
        if not self.destination_dir.exists():
            self.destination_dir.mkdir(parents=True, exist_ok=True)
        for item in self.destination_dir.iterdir():
            if item.is_file():
                item.unlink()

        table = Table(File(self.table_file)).as_dict()
        entire = Run(table, self.data_dir, "hsa-let-7a-5p", 1).run()[0]
        standard_proportions = entire.statistics().proportions()

        for file in self.data_dir.iterdir():
            gene = file.name.split(".")[0]
            clusters = Run(table, self.data_dir, gene, self.cluster_count).run()
            include: bool = False
            for cluster in clusters:
                if cluster.statistics().distance_score(standard_proportions) > self.cut_off_deviation_score:
                    include = True
                    break
            if not include:  # second try
                clusters = Run(table, self.data_dir, gene, self.cluster_count).run()
                for cluster in clusters:
                    if cluster.statistics().distance_score(standard_proportions) > self.cut_off_deviation_score:
                        include = True
                        break

            if include:
                print(gene + " included.")
                with (self.destination_dir / (gene + ".txt")).open("w") as result:
                    for i, cluster in enumerate(sorted(clusters, key=lambda x: x.center)):
                        result.write(str(i + 1) + " CLUSTER: " + gene + " EXPRESSION VALUE: "
                                     + str(cluster.center) + "\n")
                        statistics = cluster.statistics()
                        dct = statistics.as_dict()
                        result.write("Average Age: " + str(dct["age"]) + "\n")
                        result.write("Males: " + str(dct["sex"][Sex.MALE]) +
                                     ", " + str(float(dct["sex"][Sex.MALE]) / statistics.total)[:5]
                                     + "\n")
                        result.write("Females: " + str(dct["sex"][Sex.FEMALE]) +
                                     ", " + str(float(dct["sex"][Sex.FEMALE]) / statistics.total)[:5]
                                     + "\n")
                        result.write("NO APOE4: " + str(dct["apoe4"][0]) +
                                     ", " + str(float(dct["apoe4"][0]) / statistics.total)[:5]
                                     + "\n")
                        result.write("1 APOE4: " + str(dct["apoe4"][1]) +
                                     ", " + str(float(dct["apoe4"][1]) / statistics.total)[:5]
                                     + "\n")
                        result.write("2 APOE4: " + str(dct["apoe4"][2]) +
                                     ", " + str(float(dct["apoe4"][2]) / statistics.total)[:5]
                                     + "\n")
                        result.write("DIAGNOSIS AD: " + str(dct["diagnosis"]["ad"]) +
                                     ", " + str(float(dct["diagnosis"]["ad"]) / statistics.total)[:5]
                                     + "\n")
                        result.write("DIAGNOSIS DLB: " + str(dct["diagnosis"]["dlb"]) +
                                     ", " + str(float(dct["diagnosis"]["dlb"]) / statistics.total)[:5]
                                     + "\n")
                        result.write("DIAGNOSIS MCI: " + str(dct["diagnosis"]["mci"]) +
                                     ", " + str(float(dct["diagnosis"]["mci"]) / statistics.total)[:5]
                                     + "\n")
                        result.write("DIAGNOSIS NC: " + str(dct["diagnosis"]["nc"]) +
                                     ", " + str(float(dct["diagnosis"]["nc"]) / statistics.total)[:5]
                                     + "\n")
                        result.write("DIAGNOSIS VAD: " + str(dct["diagnosis"]["vad"]) +
                                     ", " + str(float(dct["diagnosis"]["vad"]) / statistics.total)[:5]
                                     + "\n")
                        result.write("TOTAL: " + str(statistics.total) + "\n")
                        result.write("\n")
            else:
                print(gene + " not included.")
