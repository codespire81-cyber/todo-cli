#!/usr/bin/env python3
"""A simple command-line task manager."""
import argparse
import json
from pathlib import Path

DB = Path.home() / ".todo_cli.json"


def load():
    """Load tasks from the JSON file."""
    return json.loads(DB.read_text(encoding="utf-8")) if DB.exists() else []


def save(tasks):
    """Save tasks to the JSON file."""
    DB.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Task manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("text")
    sub.add_parser("list", help="show all tasks")
    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int)
    rm = sub.add_parser("rm", help="remove a task")
    rm.add_argument("id", type=int)

    args = parser.parse_args()
    tasks = load()

    if args.cmd == "add":
        tasks.append({"text": args.text, "done": False})
        save(tasks)
        print(f"Added: {args.text}")
    elif args.cmd == "list":
        if not tasks:
            print("No tasks.")
        for i, t in enumerate(tasks, 1):
            print(f"{i}. [{'x' if t['done'] else ' '}] {t['text']}")
    elif args.cmd in ("done", "rm"):
        if not 1 <= args.id <= len(tasks):
            print("No task with that number.")
            return
        if args.cmd == "done":
            tasks[args.id - 1]["done"] = True
        else:
            tasks.pop(args.id - 1)
        save(tasks)
        print("Done.")


if __name__ == "__main__":
    main()
