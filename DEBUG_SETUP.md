# PyCharm Debug Setup for CareerPython

This guide explains how to set up debugging in PyCharm for the CareerPython FastAPI application.

## Overview

The project runs FastAPI locally using `uvicorn` with hot reload, while Docker provides services (PostgreSQL, Redis, etc.). This setup allows for easy debugging with PyCharm's built-in debugger.

## Prerequisites

1. PyCharm Professional (Community Edition has limited debugging features for web apps)
2. Python 3.13 installed
3. Virtual environment set up (`uv venv`)
4. Docker and Docker Compose installed

## Step 1: Configure Python Interpreter

1. Open PyCharm and load the CareerPython project
2. Go to **Settings/Preferences** → **Project: CareerPython** → **Python Interpreter**
3. Click the gear icon → **Add Interpreter** → **Add Local Interpreter**
4. Select **Virtualenv Environment** → **Existing**
5. Set the interpreter path to: `/Users/juanmacias/Projects/CareerPython/.venv/bin/python`
6. Click **OK**

## Step 2: Create Run/Debug Configuration for FastAPI

### Method A: Using PyCharm's FastAPI Template (Recommended)

1. Go to **Run** → **Edit Configurations**
2. Click **+** → **FastAPI**
3. Configure:
   - **Name**: `FastAPI Debug`
   - **Module name**: Leave as `uvicorn`
   - **Application**: `main:app`
   - **Host**: `0.0.0.0`
   - **Port**: `8000`
   - **Additional options**: `--reload`
   - **Python interpreter**: Select your `.venv` interpreter
   - **Working directory**: `/Users/juanmacias/Projects/CareerPython`
   - **Environment variables**: Add necessary env vars (see below)
4. Click **OK**

### Method B: Using Python Configuration (Alternative)

1. Go to **Run** → **Edit Configurations**
2. Click **+** → **Python**
3. Configure:
   - **Name**: `FastAPI Debug`
   - **Module name**: Select **Module** radio button, enter `uvicorn`
   - **Parameters**: `main:app --host 0.0.0.0 --port 8000 --reload`
   - **Python interpreter**: Select your `.venv` interpreter
   - **Working directory**: `/Users/juanmacias/Projects/CareerPython`
   - **Environment variables**: Click folder icon to add env vars (see below)
4. Click **OK**

### Environment Variables to Add

```
POSTGRES_USER=<from your .env>
POSTGRES_PASSWORD=<from your .env>
POSTGRES_DB=<from your .env>
POSTGRES_HOST=localhost
POSTGRES_PORT=5442
SECRET_KEY=<from your .env>
REDIS_HOST=localhost
REDIS_PORT=6399
PYTHONPATH=/Users/juanmacias/Projects/CareerPython
```

**Note**: You can load from `.env` file automatically:
- In the Environment Variables dialog, click **Load from file**
- Select your `.env` file
- Adjust `POSTGRES_HOST` and `POSTGRES_PORT` if needed (Docker exposes on 5442)

## Step 3: Start Docker Services

Before debugging, start the required services:

```bash
make start  # This will fail to start FastAPI (expected) but will start Docker services
# OR manually:
docker-compose up -d
```

**Important**: Don't use `make start` for debugging because it tries to run uvicorn in the shell. Instead:

1. Start only Docker services: `docker-compose up -d`
2. Then use PyCharm's debug configuration to run FastAPI

## Step 4: Set Breakpoints and Debug

1. Open any Python file (e.g., `adapters/http/company_app/interview/routers/company_interview_router.py`)
2. Click in the gutter (left of line numbers) to set breakpoints
3. Click the **Debug** button (bug icon) or press `Shift+F9`
4. Make API requests to trigger breakpoints
5. Use PyCharm's debug controls:
   - **F8**: Step over
   - **F7**: Step into
   - **Shift+F8**: Step out
   - **F9**: Resume program

## Step 5: Advanced Debugging Features

### Hot Reload with Debugging

The `--reload` flag works with the debugger. When you modify code:
- Uvicorn will reload automatically
- Debugger will reconnect
- Breakpoints remain active

### Debug Console

While debugging, you can:
- Evaluate expressions in the **Debug Console**
- Inspect variables in the **Variables** pane
- View call stack in the **Frames** pane

### Conditional Breakpoints

Right-click on a breakpoint to add conditions:
- Break only when `user_id == "specific_id"`
- Break only when exception occurs
- Log message without stopping execution

### Remote Debugging (Docker-based, Optional)

If you prefer running FastAPI in Docker with debugging:

1. Install `debugpy` in your container:
   ```bash
   uv add debugpy
   ```

2. Update `docker-compose.yml` to add web service:
   ```yaml
   web:
     build: .
     ports:
       - "8000:8000"
       - "5678:5678"  # Debug port
     volumes:
       - .:/code
     environment:
       - PYTHONPATH=/code
     depends_on:
       - db
       - redis
     command: python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Create Remote Debug configuration in PyCharm:
   - **Run** → **Edit Configurations** → **+** → **Python Debug Server**
   - **Port**: 5678
   - **Host**: localhost

## Step 6: Common Issues and Solutions

### Issue: Debugger doesn't stop at breakpoints
- Verify the code is actually being executed
- Check if breakpoint is in reachable code path
- Ensure interpreter is correctly configured

### Issue: Import errors or module not found
- Check `PYTHONPATH` is set to project root
- Verify virtual environment is activated
- Check interpreter is using `.venv`

### Issue: Database connection errors
- Ensure Docker services are running: `docker-compose ps`
- Check port mapping (5442 for PostgreSQL)
- Verify environment variables

### Issue: Hot reload stops working
- Restart debug session
- Check file system watcher limits (Linux)
- Ensure working directory is correct

## Best Practices

1. **Start Services First**: Always start Docker services before debugging
2. **Use Breakpoints Wisely**: Too many breakpoints slow down execution
3. **Check Logs**: View Docker logs with `make logs` for service issues
4. **Clean Restart**: If issues persist, stop all services and restart:
   ```bash
   make stop
   docker-compose up -d
   # Then start debug session in PyCharm
   ```

## Debugging Tests

To debug tests in PyCharm:

1. Right-click on test file or test function
2. Select **Debug 'pytest for test_...'**
3. PyCharm will automatically:
   - Use pytest configuration
   - Set up proper environment
   - Stop at breakpoints in test code

## Alternative: VS Code Debugging

If you prefer VS Code, create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
      ],
      "jinja": true,
      "justMyCode": false,
      "envFile": "${workspaceFolder}/.env",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ]
}
```

## Summary

Your current setup is optimal for debugging:
- FastAPI runs locally with full PyCharm debugging support
- Docker provides isolated services (DB, Redis, etc.)
- Hot reload works seamlessly with debugger
- No complex Docker debugging configuration needed

For daily development:
1. `docker-compose up -d` - Start services
2. Start PyCharm debug session - Run FastAPI with debugging
3. Set breakpoints and debug
4. `make stop` - Stop services when done