# Todo Application - Phase 1

A beautiful, modern CLI-based todo application built with Python and enhanced with the Rich library for stunning terminal output.

## Features

- Add, view, update, and delete tasks
- Mark tasks as complete or incomplete
- Beautiful color-coded interface with emojis
- Modern panels, tables, and styled text
- Interactive prompts with validation
- In-memory task storage

## Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd hackathon-todo-phase1
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install Rich directly:
   ```bash
   pip install rich
   ```

## Usage

### Recommended Way (Windows-compatible with emojis):

```bash
python run_todo.py
```

This startup script automatically configures UTF-8 encoding for proper emoji display on Windows.

### Alternative Methods:

From the project root:
```bash
python src/main.py
```

Or using module syntax:
```bash
python -m src.main
```

**Note for Windows users:** If emojis don't display correctly, use `run_todo.py` or run:
```bash
chcp 65001
python src/main.py
```

## Application Features

### Welcome Banner
A colorful ASCII art banner greets you on startup, setting the tone for a delightful user experience.

### Main Menu
Navigate through a beautifully styled menu with emojis and colored text:
- ➕ Add Task
- 📋 View Tasks
- ✏️ Update Task
- ❌ Delete Task
- ✅ Mark Complete
- 🔄 Mark Incomplete
- 🚪 Exit

### Task Operations

#### Adding Tasks
Create new tasks with titles and optional descriptions. Input validation ensures data quality.

#### Viewing Tasks
Tasks are displayed in a beautiful Rich table with:
- Color-coded status indicators
- Green ✅ for completed tasks
- Yellow ⏳ for pending tasks
- Organized columns for ID, Title, Description, and Status

#### Updating Tasks
Modify existing tasks with guided prompts showing current values.

#### Deleting Tasks
Remove tasks with clear confirmation and feedback.

#### Marking Complete/Incomplete
Toggle task completion status with visual success indicators.

### Visual Design

The application uses:
- **Cyan** for menu borders and prompts
- **Magenta** for titles and headers
- **Green** for success messages and completed tasks
- **Yellow** for pending tasks and warnings
- **Red** for error messages
- **White** for general content

## Project Structure

```
hackathon-todo-phase1/
├── src/
│   ├── domain/
│   │   └── task.py           # Task domain model
│   ├── state/
│   │   └── task_store.py     # In-memory state manager
│   ├── cli/
│   │   ├── display.py        # Rich-enhanced display functions
│   │   ├── handlers.py       # Operation handlers
│   │   └── menu.py           # Main menu loop
│   └── main.py               # Application entry point
├── specs/
│   └── 001-phase1-inmemory-cli/
│       ├── spec.md           # Feature specification
│       ├── plan.md           # Implementation plan
│       ├── tasks.md          # Development tasks
│       └── rich-ui-design.md # UI flow design document
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Technical Details

### Dependencies
- **Rich** (>=13.0.0): For beautiful terminal output
  - Panels for bordered sections
  - Tables for structured task display
  - Styled text with colors and emojis
  - Interactive prompts

### Architecture
- **Domain Layer**: Task model with business logic
- **State Layer**: In-memory storage and CRUD operations
- **CLI Layer**: User interface with Rich-enhanced display
- **Entry Point**: Application initialization and error handling

## Development

### Running Tests
(Test suite to be added in future phases)

### Code Style
- Follows PEP 8 guidelines
- Type hints for better code clarity
- Comprehensive docstrings

## Future Enhancements (Planned Phases)

- Persistent storage (JSON/Database)
- Task priorities and categories
- Due dates and reminders
- Search and filter functionality
- Export/import capabilities

## License

This is a educational project created for learning purposes.

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) by Textualize
- Developed following Spec-Driven Development principles
