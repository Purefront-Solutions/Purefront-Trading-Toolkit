import argparse

from cli.commands.collection import cmd_collection, cmd_collection_add, cmd_collection_init, cmd_collection_list, cmd_collection_remove, cmd_collection_run, cmd_collection_update
from cli.parsers import _iso8601


def build_collection_parser(subparsers: argparse._SubParsersAction) -> None:
    collection = subparsers.add_parser("collection", help="manage collections")
    collection.set_defaults(func=cmd_collection, collection_parser=collection)
    collection_subparsers = collection.add_subparsers(dest="collection_command", metavar="COMMAND")

    collection_add = collection_subparsers.add_parser("add", help="add a collection")
    collection_add.add_argument("--name", required=True, help="collection name")
    collection_add.add_argument("--database", required=True, help="database name")
    collection_add.add_argument("--datasource", required=True, help="datasource name")
    collection_add.add_argument("--query", required=True, help="query name")
    collection_add.add_argument("--type", required=True, choices=["crypto-historical-bars", "assets"], help="collection type")
    collection_add.add_argument("--frequency", choices=["1m", "1d"], help="data frequency")
    collection_add.add_argument("--start", required=True, type=_iso8601, help="start datetime (ISO 8601)")
    collection_add.add_argument("--end", type=_iso8601, help="end datetime (ISO 8601)")
    collection_add.add_argument("--symbols", type=lambda s: [x.strip() for x in s.split(",")], help="comma-separated list of symbols")
    collection_add.set_defaults(func=cmd_collection_add)

    collection_update = collection_subparsers.add_parser("update", help="update a collection")
    collection_update.add_argument("--name", required=True, help="collection name")
    collection_update.add_argument("--database", default=None, help="database name")
    collection_update.add_argument("--datasource", default=None, help="datasource name")
    collection_update.add_argument("--query", default=None, help="query name")
    collection_update.add_argument("--type", default=None, choices=["crypto-historical-bars", "assets"], help="collection type")
    collection_update.add_argument("--frequency", default=None, choices=["1m", "1d"], help="data frequency")
    collection_update.add_argument("--start", default=None, type=_iso8601, help="start datetime (ISO 8601)")
    collection_update.add_argument("--end", default=None, type=_iso8601, help="end datetime (ISO 8601)")
    collection_update.add_argument("--symbols", default=None, type=lambda s: [x.strip() for x in s.split(",")], help="comma-separated list of symbols")
    collection_update.set_defaults(func=cmd_collection_update)

    collection_list = collection_subparsers.add_parser("list", help="list collections")
    collection_list.set_defaults(func=cmd_collection_list)

    collection_remove = collection_subparsers.add_parser("remove", help="remove a collection")
    collection_remove.add_argument("--name", required=True, help="collection name")
    collection_remove.set_defaults(func=cmd_collection_remove)

    collection_init = collection_subparsers.add_parser("init", help="initialize a collection")
    collection_init.add_argument("--name", required=True, help="collection name")
    collection_init.set_defaults(func=cmd_collection_init)

    collection_run = collection_subparsers.add_parser("run", help="run a collection")
    collection_run.add_argument("--name", required=True, help="collection name")
    collection_run.set_defaults(func=cmd_collection_run)
