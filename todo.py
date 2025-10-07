from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from pathlib import Path
import argparse
from typing import Iterable 

DB_PATH = Path("todo.sqllite3")

# database helpers

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn 

def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0 
            );
            """
    )
        
# domain model
@dataclass(slots=True)    
class Task:
    id: int | None
    title: str 
    done: bool = False 

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Task":
        return cls(id=row["id"], title=row["title"], done=bool(row["done"]))
    
    def mark_done(self) -> None:
        self.done = True 

# --- data access layer 
class TaskRepo:

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_task(self, title: str) -> Task:
        
        cur = self.conn.execute(
            "INSERT INTO tasks (title, done) VALUES(?, ?)", (title, 0)
        )

        task_id = cur.lastrowid

        return Task(id=task_id, title=title, done=False)
    
    def list_tasks(self, show_all: bool = True) -> list[Task]:

        if show_all:
            
            rows = self.conn.execute(
                "SELECT id, title, done FROM tasks ORDER BY done, id"
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id, title, done FROM tasks WHERE done = 0 ORDER BY id"
            ).fetchall()

        return [Task.from_row(r) for r in rows]

    def set_done(self, task_id: int) -> bool:

        cur = self.conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id)
        )

        return cur.rowcount > 0

    def delete(self, task_id: int) -> bool:

        cur = self.conn.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id)
        )

        return cur.rowcount > 0
    
# presentation layer - cli layer


def format_tasks(tasks: Iterable[Task]) -> str:
    lines = []

    for t in tasks:
        status = "✔" if t.done else "•"
        lines.append(f"{t.id:>3} {status} {t.title}")

    return "\n".join(lines) if lines else "(no tasks)"

def cmd_add(args: argparse.Namespace) -> None:

    with get_conn() as conn:
        repo = TaskRepo(conn)
        task = repo.add_task(args.title)

    print(f"Added tasks: [{task.id}] {task.title}")

def cmd_list_tasks(args: argparse.Namespace) -> None:

    with get_conn() as conn:

        repo = TaskRepo(conn)
        tasks = repo.list_tasks(show_all=args.all)

    print(format_tasks(tasks))


def cmd_done(args: argparse.Namespace) -> None:

    with get_conn() as conn:
        repo = TaskRepo(conn)
        ok = repo.set_done(args.id)

    print("Marked done." if ok else "Task not found.")

def cmd_delete(args:argparse.Namespace) -> None:
    
    with get_conn() as conn:
        repo = TaskRepo(con)
        ok = repo.delete(args.id)

    print("Deleted." if ok else "Task not found.")


def build_parser() -> argparse.ArgumentParser:

    p = argparse.ArgumentParser(prog="todo", description="CLI To-Do App")
    sub = p.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task title")
    add_p.set_defaults(func=cmd_add)

    list_p = sub.add_parser("list", help="List Tasks")
    list_p.add_argument("--all", action="store_true", help="Show done tasks too")
    list_p.set_defaults(func=cmd_list_tasks)

    done_p = sub.add_parser("done", help="Mark task done by id")
    done_p.add_argument("id", type=int)
    done_p.set_defaults(func=cmd_done)

    del_p = sub.add_parser("delete", help="Delete tasks by id")
    del_p.add_argument("id", type=int)
    del_p.set_defaults(func=cmd_delete)

    return p 


def main() -> None:

    # ensure db exists
    init_db()

    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

