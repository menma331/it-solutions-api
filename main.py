import argparse

import uvicorn

from app import app
from db import db_manager


def init_fixtures():
    db_manager.init_fixtures()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script functions")
    parser.add_argument(
        "command", choices=["init_fixtures", "start"], help="Command to execute"
    )
    args = parser.parse_args()

    if args.command == "init_fixtures":
        init_fixtures()
    if args.command == "start":
        uvicorn.run("main:app", reload=True)
