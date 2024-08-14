from shutil import move, copy
from os import path, listdir
from typing import Callable
from pprint import pprint
import subprocess
import csv


class Localization:
    PARSER = path.join("scripts", "UnrealLocres.exe")
    DATA = "data"
    BASE_CSV = path.join(DATA, "!base.csv")
    OTHER_CSV = path.join(DATA, "~other.csv")

    def __init__(self, ignore_warnings: bool = False):
        self.ignore_warnings = ignore_warnings

    def _export_csv(self, target: str, directory: str = "."):
        """
        Run the UnrealLocres.exe script to obtain a .csv representation of the target.locres file.
        The format of the csv file is: <key>,<value>,<*empty*>
        """
        csv_file = path.join(directory, f"{path.basename(target)}.csv")

        rc = subprocess.Popen(f"{self.PARSER} export {target} -o {csv_file} -f csv", shell=True).wait()
        if rc:
            raise RuntimeError("Failed to parse .locres file to .csv")
        return csv_file

    def _import_csv(self, target: str, csv_file: str, dst: str):
        """
        Run the UnrealLocres.exe script to patch the target.locres file with the provided .csv
        """
        rc = subprocess.Popen(f"{self.PARSER} import {target} {csv_file} -f csv -o {dst}", shell=True).wait()
        if rc:
            raise RuntimeError("Failed to patch the .locres file")
        return csv_file

    @staticmethod
    def _read_csv(path: str):
        with open(path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return {row["key"]: (row["source"], row["target"]) for row in reader}

    @classmethod
    def _get_all_csv(cls):
        csv_list = [path.join(cls.DATA, file) for file in listdir(cls.DATA)
                    if path.isfile(path.join(cls.DATA, file)) and file.endswith(".csv")]
        return sorted(csv_list)

    def _update_all_csv(self, source_csv: str):
        """
        Update all of .csv files, since the new localization might have some fields updated.
        Any new keys are added to the end of ~other.csv
        """
        move(source_csv, self.BASE_CSV)  # update the base.csv
        new_loc = self._read_csv(self.BASE_CSV)
        keys_without_translation = set(new_loc.keys())  # remember which keys were added
        removed_keys = set()  # remember which keys were removed
        csv_list = self._get_all_csv()[1:]  # list of all csv files without !base.csv

        for csv_path in csv_list:  # iterate over all csv files
            old_loc = self._read_csv(csv_path)
            with open(csv_path, newline="", encoding="utf-8", mode="w") as csv_file:
                writer = csv.writer(csv_file, lineterminator="\n")
                writer.writerow(["key", "source", "target"])
                for key, (source, target) in old_loc.items():
                    try:
                        keys_without_translation.remove(key)  # update list of new keys
                        # write the rows back to the same file,
                        # but with the source from the new .locres
                        # python will preserve the key order in the dict
                        writer.writerow([key, new_loc[key][0], target])
                    except KeyError:
                        removed_keys.add(key)  # update list of removed keys

        # write any new keys to the end of ~other.csv
        # the translation should be added by hand
        with open(csv_list[-1], newline="", encoding="utf-8", mode="a") as f:
            writer = csv.writer(f, lineterminator="\n")
            for key in keys_without_translation:
                writer.writerow([key, new_loc[key][0], ""])

        if removed_keys:
            print("WARN: these keys were removed in the latest version:")
            pprint(removed_keys)

    def patch(self, target: str, output: str, filter_csv: Callable[[str], bool] = None):
        """
        Use the .csv files to patch the base .locres
        The .csv files are applied in order, so the last .csv will override any previous changes
        """
        csv_list = self._get_all_csv()
        if filter_csv is not None:
            csv_list = filter(filter_csv, csv_list)

        copy(target, output)
        for csv in csv_list:
            self._import_csv(output, csv, output)

    def migrate(self, target_locres: str, source_locres: str):
        """
        Copies the source.locres over the target.locres
        Updates all .csv files using the new .locres
        Any new keys are added to the end of ~other.csv
        """
        # validate user input
        if any(not file or not path.isfile(file) for file in [target_locres, source_locres]):
            raise FileNotFoundError("target and source are required")

        source_csv = self._export_csv(source_locres)  # export new locres to csv
        self._update_all_csv(source_csv)  # update all csv with new original localization
        copy(source_locres, target_locres)  # use source as the new target


if __name__ == "__main__":
    print("Please use the main.py script")
    exit(1)
