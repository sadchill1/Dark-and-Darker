from shutil import move, copy
from os import path, listdir
import subprocess
import tempfile


class Localization:
    PARSER=path.join("scripts", "UnrealLocres.exe")
    DATA="data"

    def __init__(self, ignore_warnings: bool = False):
        self.ignore_warnings = ignore_warnings

    @staticmethod
    def _backup_name(f: str):
        return f + ".bak"

    @staticmethod
    def _escape(string:str):
        if '"' in string:
            string = string.replace('"', "‘")
        if "\n" in string or "," in string:
            return f'"{string}"'
        return string

    def _export_csv(self, target: str, directory: str):
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

    def patch(self, target: str, output: str):
        """
        Use the .csv files to patch the base .locres
        The .csv files are applied in order, so the last .csv will override any previous changes
        """
        csv_list = [path.join(self.DATA, file) for file in listdir(self.DATA)
                    if path.isfile(path.join(self.DATA, file)) and file.endswith(".csv")]
        csv_list.sort()
        with tempfile.TemporaryDirectory() as temp_dir:
            locres = path.join(temp_dir, "tmp.locres")
            copy(target, locres)
            for csv in csv_list:
                self._import_csv(locres, csv, locres)
            move(locres, output)

    def migrate(self, target: str, source: str, base_csv: str):
        """
        Creates a backup of the target.locres
        Copies the source.locres over the target.locres
        Updates the base.csv using the new .locres
        """
        # validate user input
        if any(not file or not path.isfile(file) for file in [target, source, base_csv]):
            raise FileNotFoundError("target, source, and base_csv are required")
        # check that we won't corrupt any backups
        if any(path.isfile(self._backup_name(file)) for file in [target, base_csv]) and \
           not self.ignore_warnings:
            #
            raise FileExistsError("Please make sure that your backup files are not overriden")

        # create a temp dir to store csv files
        with tempfile.TemporaryDirectory() as temp_dir:
            source_csv = self._export_csv(source, temp_dir)
            target_csv = self._export_csv(target, temp_dir)
            move(target, self._backup_name(target))  # create a backup
            move(base_csv, self._backup_name(base_csv))  # create a backup
            copy(source, target)  # use source as the new target
            move(source_csv, base_csv)  # update the base.csv

if __name__ == "__main__":
    print("Please use the main.py script")
    exit(1)
