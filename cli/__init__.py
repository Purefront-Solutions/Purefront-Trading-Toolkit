import argparse
import sys

from dotenv import load_dotenv

from cli.commands.version import cmd_version
from cli.parsers.collection_parser import build_collection_parser
from cli.parsers.database_parser import build_database_parser
from cli.parsers.datasource_parser import build_datasource_parser
from cli.parsers.query_parser import build_query_parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ttk",
        description="Historical Data Collector CLI",
    )
    parser.add_argument("--version", dest="show_version", action="store_true", help="show version")
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = False
    build_database_parser(subparsers)
    build_datasource_parser(subparsers)
    build_collection_parser(subparsers)
    build_query_parser(subparsers)
    return parser


def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()
    if args.show_version:
        cmd_version(args)
    elif args.command is None:
        parser.print_help()
        sys.exit(1)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
