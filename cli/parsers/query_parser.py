import argparse

from cli.commands.query import cmd_query, cmd_query_add, cmd_query_list, cmd_query_remove, cmd_query_update
from cli.parsers import _iso8601


def build_query_parser(subparsers: argparse._SubParsersAction) -> None:
    query = subparsers.add_parser("query", help="manage queries")
    query.set_defaults(func=cmd_query, query_parser=query)
    query_subparsers = query.add_subparsers(dest="query_command", metavar="COMMAND")

    query_add = query_subparsers.add_parser("add", help="add a query")
    query_add.add_argument("--name", required=True, help="query name")
    query_add.add_argument("--type", required=True, help="query type")
    query_add.add_argument("--symbols", type=lambda s: [x.strip() for x in s.split(",")], help="comma-separated list of symbols")
    query_add.add_argument("--frequency", choices=["1m", "1d"], help="data frequency")
    query_add.add_argument("--start", type=_iso8601, help="start datetime (ISO 8601)")
    query_add.add_argument("--end", type=_iso8601, help="end datetime (ISO 8601)")
    query_add.add_argument("--asset-class", dest="asset_class", default=None, help="asset class filter")
    query_add.add_argument("--status", default=None, help="asset status filter")
    query_add.set_defaults(func=cmd_query_add)

    query_update = query_subparsers.add_parser("update", help="update a query")
    query_update.add_argument("--name", required=True, help="query name")
    query_update.add_argument("--symbols", default=None, type=lambda s: [x.strip() for x in s.split(",")], help="comma-separated list of symbols")
    query_update.add_argument("--frequency", default=None, choices=["1m", "1d"], help="data frequency")
    query_update.add_argument("--start", default=None, type=_iso8601, help="start datetime (ISO 8601)")
    query_update.add_argument("--end", default=None, type=_iso8601, help="end datetime (ISO 8601)")
    query_update.add_argument("--asset-class", dest="asset_class", default=None, help="asset class filter")
    query_update.add_argument("--status", default=None, help="asset status filter")
    query_update.set_defaults(func=cmd_query_update)

    query_list = query_subparsers.add_parser("list", help="list queries")
    query_list.set_defaults(func=cmd_query_list)

    query_remove = query_subparsers.add_parser("remove", help="remove a query")
    query_remove.add_argument("--name", required=True, help="query name")
    query_remove.set_defaults(func=cmd_query_remove)
