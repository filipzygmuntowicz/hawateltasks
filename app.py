from task_hawatel import tasks
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', help="""
    task name, choose from: update_prices, excel, both (default is both)""")
    parser.add_argument('--username', help="""
    your username""")
    parser.add_argument("--password", help="""
    your password""")
    parser.add_argument("--host", help="""
    database host""")
    parser.add_argument("--db_name", help="""
    name of the database""")
    args = parser.parse_args()
    if args.username is not None and\
            args.host is not None and\
            args.db_name is not None:
        if args.password is None:
            op = tasks.Operations(
                args.username, "", args.host, args.db_name)
        else:
            op = tasks.Operations(
                args.username, args.password, args.host, args.db_name)
    else:
        op = tasks.Operations()
    if args.task is None or args.task == "both":
        op.update_prices()
        op.excel()
    elif args.task == "excel":
        op.excel()
    elif args.task == "update_prices":
        op.update_prices()
