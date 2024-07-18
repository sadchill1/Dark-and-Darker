from scripts.localization_tool import Localization
from os import path
import argparse


ACTION_MIGRATE="migrate"
ACTION_PATCH="patch"


def parse_args():
    prog = path.basename(__file__)
    parser = argparse.ArgumentParser(
            prog=prog,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="This tool assists in migrating localizations between different versions "
                        "and allows for patching base locres files.",
            epilog="examples:\n"
                  f"\t{prog} {ACTION_MIGRATE} --target ./data/Game.locres --source Game_new.locres --base-csv=./data/!base.csv\n"
                  f"\t{prog} {ACTION_PATCH} --target ./data/Game.locres --output patched.locres\n")

    parser.add_argument("action", type=str, choices=[ACTION_MIGRATE, ACTION_PATCH])
    parser.add_argument("--target", "-t", metavar="<TARGET.locres>", type=str,
                        default=path.join("data", "Game.locres"),
                        help="target .locres file (default: ./data/Game.locres)")
    parser.add_argument("--source", "-s", metavar="<SOURCE.locres>", type=str,
                        help="source .locres file")
    parser.add_argument("--base-csv", "-b", metavar="<BASE.csv>", type=str,
                        default=path.join("data", "!base.csv"),
                        help="name of the base .csv file which is used as a template (default: ./data/!base.csv)")
    parser.add_argument("--output", "-o", metavar="<OUT.locres>", type=str,
                        default="patched.locres",
                        help="name of the ouptut .locres file after migration or patching (default: ./patched.locres)")
    parser.add_argument("--added-keys", metavar="<ADDED_KEYS.txt>", type=str,
                        default="added_keys.txt",
                        help="location where the new keys are added after the migration")
    parser.add_argument("--force", action="store_true", help="ignore warnings")

    return parser.parse_args()


def main():
    args = parse_args()
    try:
        if args.action == ACTION_MIGRATE:
            Localization(args.force).migrate(args.target, args.source, args.base_csv, args.added_keys)
        if args.action == ACTION_PATCH:
            Localization(args.force).patch(args.target, args.output)
    except (ValueError, FileNotFoundError, FileExistsError) as e:
        print("ERROR:")
        print(str(e))
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
