import argparse

def main():

    parser = argparse.ArgumentParser(description="Test CLI")
    sub = parser.add_subparsers(dest="command", required=False)

    add_p = sub.add_parser("add", help="Add a task")
    add_p.add_argument("title", help="Task title")

    args = parser.parse_args()
    if not args.command:
        print("No command given. Use --help for usege.")
    else:
        print(f"Command: {args.command}, title: {getattr(args, 'title', None)}")
    

if __name__ == "__main__":
    main()

