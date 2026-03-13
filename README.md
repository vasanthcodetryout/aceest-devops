# ACEest Fitness & Gym — DevOps CI/CD Pipeline

> **Course:** Introduction to DevOps
> **Assignment:** Automated CI/CD Pipeline Implementation

---

## Project Overview

This project is a **Flask REST API** for the ACEest Fitness & Gym management system, wrapped in a complete DevOps pipeline using:

| Tool | Purpose |
|---|---|
| **Git / GitHub** | Version control & remote repository |
| **Flask** | Web application framework (Python) |
| **Pytest** | Automated unit testing |
| **Docker** | Containerization |
| **GitHub Actions** | Automated CI/CD pipeline |
| **Jenkins** | Secondary BUILD validation |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check — confirms app is running |
| `GET` | `/programs` | List all fitness programs |
| `GET` | `/program/<name>` | Get workout + diet plan for a program |
| `GET` | `/clients` | List all saved clients |
| `POST` | `/clients` | Add a new client |
| `GET` | `/calories?weight=X&program=Y` | Calculate daily calorie target |

---

## Local Setup & Execution

### Prerequisites
- Python 3.11+
- pip
- Docker Desktop (for container steps)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/aceest-devops.git
cd aceest-devops
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the Flask App
```bash
python app.py
```
App will start at: **http://localhost:5000**

### Step 4 — Test the API (use curl or browser)
```bash
# Health check
curl http://localhost:5000/

# Get all programs
curl http://localhost:5000/programs

# Get Fat Loss program details
curl "http://localhost:5000/program/Fat Loss (FL)"

# Calculate calories
curl "http://localhost:5000/calories?weight=75&program=Muscle Gain (MG)"

# Add a client
curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name": "Arjun", "age": 28, "weight": 75, "program": "Muscle Gain (MG)"}'
```

---

## Running Tests Manually

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run a specific test class
pytest tests/test_app.py::TestClients -v

# Run with coverage report
pip install pytest-cov
pytest tests/ -v --cov=app --cov-report=term-missing
```

Expected output: **All tests should pass (PASSED)**

---

## Docker — Build & Run

### Build the Image
```bash
docker build -t aceest-fitness .
```

### Run the Container
```bash
docker run -p 5000:5000 aceest-fitness
```
App is available at **http://localhost:5000**

### Run Tests Inside the Container
```bash
docker run --rm aceest-fitness pytest tests/ -v
```

### Useful Docker Commands
```bash
# List images
docker images

# List running containers
docker ps

# Stop a container
docker stop <container_id>

# Remove image
docker rmi aceest-fitness
```

---

## GitHub Actions — CI/CD Pipeline

### How It Works
Every `git push` to `main` automatically triggers this pipeline on GitHub's servers:

```
Push to main
     │
     ▼
┌─────────────────────┐
│  Job 1: Build+Test  │
│  ─────────────────  │
│  1. Checkout code   │
│  2. Install Python  │
│  3. pip install     │
│  4. flake8 lint     │  ← Fails fast if syntax errors
│  5. pytest suite    │  ← Fails if any test fails
└────────┬────────────┘
         │ (only if Job 1 passes)
         ▼
┌─────────────────────┐
│  Job 2: Docker      │
│  ─────────────────  │
│  1. docker build    │
│  2. pytest in       │
│     container       │
│  3. Smoke test      │  ← curl localhost:5000
└─────────────────────┘
```

### Viewing Results
1. Go to your GitHub repository
2. Click the **Actions** tab
3. Click on any workflow run to see detailed logs

A **green checkmark ✅** = all stages passed  
A **red X ❌** = something failed (click to see which step and why)

---

## Jenkins — BUILD Configuration

### Setup Steps

1. **Install Jenkins** from [jenkins.io](https://www.jenkins.io/download/)
2. Open Jenkins at `http://localhost:8080`
3. Install plugins: **Git**, **GitHub**, **Docker**
4. Create a **New Item** → **Freestyle Project** → Name: `ACEest-Build`

### Jenkins Job Configuration

**Source Code Management:**
- Repository URL: `https://github.com/YOUR_USERNAME/aceest-devops.git`
- Branch: `*/main`

**Build Triggers:**
- ☑ Poll SCM: `H/5 * * * *` (checks every 5 minutes)

**Build Steps → Execute Shell:**
```bash
echo "=== Setting up Python environment ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Running lint ==="
pip install flake8
flake8 app.py --count --select=E9,F63,F7,F82 --show-source

echo "=== Running tests ==="
pytest tests/ -v

echo "=== Building Docker image ==="
docker build -t aceest-fitness:jenkins-build .

echo "=== BUILD COMPLETE ==="
```

### Integration with GitHub Actions
- **GitHub Actions** = primary CI/CD (runs on every push, fully automated)
- **Jenkins** = secondary BUILD gate (validates in a controlled local environment)

Both must pass before code is considered "production-ready."

---

## Git Commit History

This project follows **Conventional Commits** for readable history:

```
feat:  new feature
fix:   bug fix
build: Dockerfile / dependency changes  
ci:    GitHub Actions / Jenkins changes
test:  pytest additions
docs:  README changes
```

Example commits in this project:
```
feat: add Flask REST API for ACEest fitness management
test: add 30+ pytest cases covering all endpoints and edge cases
build: add optimized slim Dockerfile with non-root user
ci: add GitHub Actions pipeline with lint, test, and docker stages
docs: add professional README with setup and CI/CD documentation
```

---

## Project Structure

```
aceest-devops/
├── app.py                        ← Flask REST API (6 endpoints)
├── requirements.txt              ← Pinned dependencies
├── Dockerfile                    ← Optimized container config
├── README.md                     ← This file
├── .github/
│   └── workflows/
│       └── main.yml              ← GitHub Actions CI/CD pipeline
└── tests/
    └── test_app.py               ← 30+ Pytest test cases
```
