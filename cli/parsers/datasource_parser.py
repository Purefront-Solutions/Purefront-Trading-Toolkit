import argparse

from cli.commands.datasource import cmd_datasource, cmd_datasource_add, cmd_datasource_list, cmd_datasource_remove, cmd_datasource_test, cmd_datasource_update


def build_datasource_parser(subparsers: argparse._SubParsersAction) -> None:
    datasource = subparsers.add_parser("datasource", help="manage datasources")
    datasource.set_defaults(func=cmd_datasource, datasource_parser=datasource)
    datasource_subparsers = datasource.add_subparsers(dest="datasource_command", metavar="COMMAND")

    datasource_add = datasource_subparsers.add_parser("add", help="add a datasource")
    datasource_add.add_argument("--name", required=True, help="datasource name")
    datasource_add.add_argument("--type", dest="datasource_type", required=True, choices=["alpaca"], help="datasource type")
    datasource_add.add_argument("--apiKey", dest="api_key", required=True, help="API key")
    datasource_add.add_argument("--apiSecret", dest="api_secret", required=True, help="API secret")
    datasource_add.set_defaults(func=cmd_datasource_add)

    datasource_update = datasource_subparsers.add_parser("update", help="update a datasource")
    datasource_update.add_argument("--name", required=True, help="datasource name")
    datasource_update.add_argument("--type", dest="datasource_type", default=None, choices=["alpaca"], help="datasource type")
    datasource_update.add_argument("--apiKey", dest="api_key", default=None, help="API key")
    datasource_update.add_argument("--apiSecret", dest="api_secret", default=None, help="API secret")
    datasource_update.set_defaults(func=cmd_datasource_update)

    datasource_list = datasource_subparsers.add_parser("list", help="list datasources")
    datasource_list.set_defaults(func=cmd_datasource_list)

    datasource_test = datasource_subparsers.add_parser("test", help="test datasource authentication")
    datasource_test.add_argument("--name", required=True, help="datasource name")
    datasource_test.set_defaults(func=cmd_datasource_test)

    datasource_remove = datasource_subparsers.add_parser("remove", help="remove a datasource")
    datasource_remove.add_argument("--name", required=True, help="datasource name")
    datasource_remove.set_defaults(func=cmd_datasource_remove)
