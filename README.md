# Proto Stack - Minimal Todo App

A minimal full stack Todo application using Streamlit for the frontend, FastAPI for the backend, and PostgreSQL for the database. The project is configured to use Docker Compose to orchestrate the entire stack for local development and debugging.

## Architecture

- **Frontend**: Streamlit (Python web app framework)
- **Backend**: FastAPI (Python web API framework)
- **Database**: PostgreSQL
- **Schema Migration**: Liquibase for versioned database changes
- **Orchestration**: Docker Compose
- **Debugging**: VS Code with Python debugger support

## Quick Start

1. **Prerequisites**: Make sure you have Docker and Docker Compose installed on your system.

2. **Clone and run**:
   ```bash
   git clone <repository-url>
   cd proto_stack
   docker compose up --build
   ```

3. **Access the application**:
   - Frontend (Streamlit): http://localhost:8501
   - Backend API (FastAPI): http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development & Debugging

### Database Migrations

The project uses Liquibase for database schema management. Database changes are versioned and applied through migration files.

**Migration Commands:**

```bash
# Apply all pending migrations
./scripts/migrate.sh update

# Check migration status
./scripts/migrate.sh status

# Validate changelog files
./scripts/migrate.sh validate

# Rollback last N migrations
./scripts/migrate.sh rollback-count <count>
```

**Migration workflow:**
1. Create new migration files in `database/liquibase/changelogs/vX.X.X/`
2. Update the master changelog to include new migration files
3. Run `./scripts/migrate.sh update` to apply changes
4. The backend service automatically waits for migrations to complete

### VS Code Setup

The project includes VS Code configuration for debugging both frontend and backend services:

1. **Start the stack**: Run `Docker Compose Up` task from VS Code Command Palette (`Ctrl+Shift+P`)
2. **Attach debugger**: Use the "Debug Full Stack" configuration to attach to both services

   For debug mode with debugger support:
   ```bash
   docker compose -f docker-compose.debug.yml up --build
   ```
   
3. **Set breakpoints**: Place breakpoints in your Python code and they will be hit during execution

### Debug Configurations Available:
- `Debug Backend (FastAPI)`: Attaches to FastAPI service on port 5678
- `Debug Frontend (Streamlit)`: Attaches to Streamlit service on port 5679  
- `Debug Full Stack`: Attaches to both services simultaneously

### Manual Docker Commands

```bash
# Start all services
docker compose up --build

# Start in background
docker compose up -d --build

# Stop all services
docker compose down

# View logs
docker compose logs

# Rebuild specific service
docker compose build backend
docker compose build frontend
```

## Project Structure

```
proto_stack/
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container config
├── frontend/               # Streamlit frontend
│   ├── app.py             # Streamlit application
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Frontend container config
├── database/              # Database configuration
│   ├── init.sql          # Database initialization
│   ├── Dockerfile.liquibase # Liquibase container config
│   └── liquibase/        # Liquibase migration files
│       ├── liquibase.properties
│       └── changelogs/   # Database changelog files
│           ├── db.changelog-master.yaml
│           └── v1.0.0/   # Version-specific migrations
├── scripts/              # Utility scripts
│   └── migrate.sh       # Database migration script
├── .vscode/              # VS Code configuration
│   ├── launch.json       # Debug configurations
│   └── tasks.json        # Build tasks
├── docker-compose.yml    # Docker Compose orchestration
├── docker-compose.override.yml # Development overrides
├── .env                  # Environment variables
└── README.md            # This file
```

## API Endpoints

The FastAPI backend provides the following REST endpoints:

- `GET /` - Health check
- `GET /todos` - List all todos
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

## Features

- ✅ Create, read, update, delete (CRUD) operations for todos
- ✅ Mark todos as complete/incomplete
- ✅ Real-time updates between frontend and backend
- ✅ PostgreSQL persistence
- ✅ **Liquibase schema migration for versioned database changes**
- ✅ Docker containerization
- ✅ VS Code debugging support
- ✅ Hot reload for development

## Screenshots

### Application Interface
The Streamlit frontend provides a clean, intuitive interface for managing todos:

![Todo App Interface](https://github.com/user-attachments/assets/d2fcd64e-83e7-4e49-8bdf-a86bdcdbb1ac)

### Working Application
Here's the application in action with multiple todos, showing the complete/incomplete functionality:

![Todo App Working](https://github.com/user-attachments/assets/dcece8b5-6d21-41ac-acd8-f407f8d855be)

## Troubleshooting

**Database connection issues**:
- Ensure PostgreSQL container is healthy: `docker-compose ps`
- Check database logs: `docker-compose logs postgres`

**Database migration issues**:
- Check migration status: `./scripts/migrate.sh status`
- Validate migration files: `./scripts/migrate.sh validate`
- View migration logs: `docker-compose logs migration-runner`
- For manual migration: `docker compose --profile migration run --rm liquibase update`

**Port conflicts**:
- Make sure ports 8000, 8501, and 5432 are not in use by other applications

**Debugging not working**:
- Ensure the debugpy ports (5678, 5679) are exposed and not blocked by firewall
- Check that the debugger is waiting for client connection before proceeding
