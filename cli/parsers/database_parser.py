import argparse

from cli.commands.database import cmd_database, cmd_database_add, cmd_database_list, cmd_database_remove, cmd_database_test, cmd_database_update


def build_database_parser(subparsers: argparse._SubParsersAction) -> None:
    database = subparsers.add_parser("database", help="manage databases")
    database.set_defaults(func=cmd_database, database_parser=database)
    database_subparsers = database.add_subparsers(dest="database_command", metavar="COMMAND")

    database_add = database_subparsers.add_parser("add", help="add a database")
    database_add.add_argument("--name", required=True, help="connection name")
    database_add.add_argument("--type", dest="db_type", required=True, help="database type")
    database_add.add_argument("--username", required=True, help="database username")
    database_add.add_argument("--password", required=True, help="database password")
    database_add.add_argument("--host", required=True, help="database host")
    database_add.add_argument("--port", type=int, required=True, help="database port")
    database_add.add_argument("--dbname", required=True, help="database name")
    database_add.set_defaults(func=cmd_database_add)

    database_update = database_subparsers.add_parser("update", help="update a database")
    database_update.add_argument("--name", required=True, help="connection name")
    database_update.add_argument("--type", dest="db_type", default=None, help="database type")
    database_update.add_argument("--username", default=None, help="database username")
    database_update.add_argument("--password", default=None, help="database password")
    database_update.add_argument("--host", default=None, help="database host")
    database_update.add_argument("--port", type=int, default=None, help="database port")
    database_update.add_argument("--dbname", default=None, help="database name")
    database_update.set_defaults(func=cmd_database_update)

    database_list = database_subparsers.add_parser("list", help="list databases")
    database_list.set_defaults(func=cmd_database_list)

    database_remove = database_subparsers.add_parser("remove", help="remove a database")
    database_remove.add_argument("--name", required=True, help="database name")
    database_remove.set_defaults(func=cmd_database_remove)

    database_test = database_subparsers.add_parser("test", help="test database connection")
    database_test.add_argument("--name", required=True, help="database name")
    database_test.set_defaults(func=cmd_database_test)
