# Hackathon II Todo Application

A full-featured todo application with both CLI and web interfaces, showcasing modern development practices from in-memory CLI to production-ready full-stack architecture.

## 🚀 Project Overview

This project demonstrates a complete software development journey:
- **Phase 1**: Beautiful CLI application with Rich UI and in-memory storage
- **Phase 2**: Full-stack web application with Next.js frontend, FastAPI backend, and PostgreSQL database

## ✨ Features

### Phase 1: CLI Application
- ✅ Add, view, update, and delete tasks
- ✅ Mark tasks as complete or incomplete
- ✅ Beautiful color-coded interface with emojis
- ✅ Modern panels, tables, and styled text
- ✅ Interactive prompts with validation
- ✅ In-memory task storage
- ✅ Advanced features: priorities, categories, due dates, recurrence, search

### Phase 2: Web Application
- 🔐 User authentication (signup/login) with Better Auth
- 👤 Multi-user support with user isolation
- 🌐 Modern Next.js 16+ frontend with App Router
- ⚡ FastAPI backend with SQLModel ORM
- 🗄️ PostgreSQL database with Neon integration
- 🐳 Docker containerization for easy deployment
- 🔑 JWT-based authentication
- 📱 Responsive web interface
- 🔄 RESTful API design

## 📦 Installation

### Prerequisites

**For Phase 1 (CLI):**
- Python 3.13 or higher
- pip (Python package installer)

**For Phase 2 (Web App):**
- Docker and Docker Compose
- Node.js 18+ (for local development without Docker)
- PostgreSQL (or Neon DB account)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/1177rashid/Hackathon_2_Todo_app.git
   cd Hackathon_2_Todo_app
   ```

### Phase 1: CLI Setup

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the CLI application:**
   ```bash
   python run_todo.py
   ```

### Phase 2: Web App Setup (Docker - Recommended)

2. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Phase 2: Local Development Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 💻 Usage

### Phase 1: CLI Application

**Recommended (Windows-compatible with emojis):**
```bash
python run_todo.py
```

**Alternative methods:**
```bash
python src/main.py
# or
python -m src.main
```

**Windows emoji fix:**
```bash
chcp 65001
python src/main.py
```

### Phase 2: Web Application

1. **Sign up for an account** at http://localhost:3000/signup
2. **Log in** at http://localhost:3000/login
3. **Create and manage tasks** through the web interface
4. **Access API documentation** at http://localhost:8000/docs

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

## 📁 Project Structure

```
Hackathon_2_Todo_app/
├── frontend/                 # Next.js 16+ frontend
│   ├── app/                  # App Router pages
│   │   ├── (auth)/          # Auth routes (login/signup)
│   │   ├── dashboard/       # Dashboard page
│   │   └── tasks/           # Tasks management
│   ├── components/          # React components
│   ├── hooks/               # Custom React hooks
│   └── types/               # TypeScript types
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── auth.py          # JWT authentication
│   │   ├── database.py      # Database connection
│   │   ├── models.py        # SQLModel models
│   │   ├── routes/          # API routes
│   │   └── main.py          # FastAPI app
│   ├── migrations/          # Alembic migrations
│   └── requirements.txt     # Python dependencies
├── src/                     # Phase 1 CLI application
│   ├── domain/              # Domain models
│   ├── state/               # State management
│   ├── cli/                 # CLI interface
│   └── main.py              # CLI entry point
├── specs/                   # Feature specifications
│   ├── 001-phase1-inmemory-cli/
│   ├── 002-web-auth-specs/
│   ├── api/                 # API specifications
│   ├── database/            # Database schemas
│   └── features/            # Feature docs
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container definition
└── README.md                # This file
```

## 🛠️ Technical Stack

### Phase 1: CLI Application
**Dependencies:**
- **Rich** (>=13.0.0): Beautiful terminal UI
- **Python** 3.13+: Core language
- **In-memory storage**: Task state management

**Architecture:**
- **Domain Layer**: Task models with business logic
- **State Layer**: In-memory CRUD operations
- **CLI Layer**: Rich-enhanced user interface
- **Validation**: Input validation and error handling

### Phase 2: Web Application
**Frontend:**
- **Next.js** 16+: React framework with App Router
- **TypeScript**: Type-safe development
- **Better Auth**: Authentication library
- **Tailwind CSS**: Styling (if configured)

**Backend:**
- **FastAPI**: Modern Python web framework
- **SQLModel**: SQL databases with Python objects
- **Alembic**: Database migrations
- **JWT**: Token-based authentication
- **PostgreSQL/Neon**: Production database

**Infrastructure:**
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Uvicorn**: ASGI server

## 🧪 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
- **Python**: PEP 8 guidelines, type hints, comprehensive docstrings
- **TypeScript**: Strict mode, ESLint configuration
- **Architecture**: Spec-Driven Development (SDD) methodology

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 🎯 Development Methodology

This project follows **Spec-Driven Development (SDD)** principles:
- ✅ Specifications written before implementation
- ✅ Architecture planning with decision records
- ✅ Task breakdown and testable acceptance criteria
- ✅ Prompt History Records (PHRs) for all changes
- ✅ Comprehensive documentation in `specs/` directory

## 🚀 Deployment

### Docker Production Build
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
Create `.env` files for backend and frontend:
```env
# Backend .env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Frontend .env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎓 Learning Objectives

This project demonstrates:
- Modern Python CLI development with Rich
- Full-stack web development (Next.js + FastAPI)
- Authentication and authorization
- Database design and migrations
- Docker containerization
- RESTful API design
- Spec-Driven Development methodology

## 📄 License

This is an educational project created for learning purposes.

## 👤 Author

**1177rashid**
- GitHub: [@1177rashid](https://github.com/1177rashid)
- Repository: [Hackathon_2_Todo_app](https://github.com/1177rashid/Hackathon_2_Todo_app)

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) by Textualize - Beautiful terminal UI
- [Next.js](https://nextjs.org/) - React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Better Auth](https://www.better-auth.com/) - Authentication library
- Developed following Spec-Driven Development principles

## 📚 Documentation

Comprehensive documentation available in the `specs/` directory:
- Phase 1 specifications: `specs/001-phase1-inmemory-cli/`
- Phase 2 specifications: `specs/002-web-auth-specs/`
- API documentation: `specs/api/`
- Database schemas: `specs/database/`
- Feature docs: `specs/features/`
