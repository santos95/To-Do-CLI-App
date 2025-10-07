# To-Do-CLI-App

A simple yet powerful Command-Line To-Do application

Features

✅ Add tasks directly from the command line

📋 List tasks (pending or completed)

✏️ Mark tasks as done

🗑️ Delete tasks by ID

💾 Persistent storage using SQLite

⚙️ Clean code design with functions, classes, and argparse

1️⃣ Clone the repository
git clone https://github.com/<your-username>/todo-cli.git
cd todo-cli

2️⃣ Create and activate a virtual environment
# Windows
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate


3️⃣ Run the application
python todo.py add "Learn Python functions"
python todo.py add "Practice classes"
python todo.py list
python todo.py done 1
python todo.py list --all


💡 Example Output
> python todo.py add "Learn argparse"
Added: [1] Learn argparse

> python todo.py list
  1  •  Learn argparse

> python todo.py done 1
Marked done.

> python todo.py list --all
  1  ✔  Learn argparse