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
    parser.add_argument("--output", "-o", metavar="<OUT.locres>", type=str,
                        default="patched.locres",
                        help="name of the ouptut .locres file after migration or patching (default: ./patched.locres)")

    return parser.parse_args()


def format_out_name(name: str):
    *suffix, file_type = name.split(".")
    if not suffix:
        suffix = [file_type]
        file_type = "locres"
    return name, ".".join(suffix) + f"_no_items.{file_type}"


def main():
    args = parse_args()
    try:
        if args.action == ACTION_MIGRATE:
            Localization().migrate(args.target, args.source)
        if args.action == ACTION_PATCH:
            patched_locres, no_items_locres = format_out_name(args.output)
            item_path = path.join(Localization.DATA, "items.csv")
            # create one .locres with all fields translated
            Localization().patch(args.target, patched_locres)
            # and one .locres with original names for the items
            Localization().patch(args.target, no_items_locres, lambda f: f != item_path)

            print(f"\nCreated patched files:\n{patched_locres}\n{no_items_locres}")
    except (ValueError, FileNotFoundError, FileExistsError) as e:
        print("ERROR:")
        print(str(e))
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
