<p align="center">
  <a href="https://MohammedRafeeq.pythonanywhere.com">
    <img src="https://img.shields.io/badge/Live_Demo-PythonAnywhere-5C4EE5?style=for-the-badge&logo=python&logoColor=white"/>
  </a>
  <br/>
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTMX-2.0-3366CC?style=for-the-badge&logo=htmx&logoColor=white"/>
  <img src="https://img.shields.io/badge/Celery-5.5-37814A?style=for-the-badge&logo=celery&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenAI-2.37-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <br/>
  <img src="https://img.shields.io/github/license/mohammedrafeeq-dev/ai-task-manager?style=flat-square"/>
  <img src="https://img.shields.io/badge/tests-19%20passing-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/coverage-72%25-yellow?style=flat-square"/>
</p>

<h1 align="center">AI-Powered Task Management SaaS</h1>

<p align="center">
  A production-ready multi-tenant task manager powered by <strong>Flask</strong>, <strong>HTMX</strong>, and <strong>OpenAI</strong> — featuring NLP task creation, smart prioritization, AI chat assistant, and auto-generated reports.
  <br/><br/>
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#docker-deployment">Docker</a> •
  <a href="#testing">Testing</a> •
  <a href="#project-structure">Structure</a>
</p>

---

## Features

| Capability | Description |
|---|---|
| **NLP Task Creation** | Describe a task in plain English — the AI extracts title, description, due date, and priority automatically |
| **Smart Prioritization** | AI analyzes task content and suggests an appropriate priority level |
| **AI Chat Assistant** | Conversational HTMX-streaming assistant that answers questions about your tasks |
| **Auto Reports** | Celery beat generates weekly AI-powered productivity reports |
| **Multi-Tenant Orgs** | Organizations with isolated data, memberships, and role-based access |
| **Auth & Sessions** | Register, login, logout with Flask-Login and secure session management |
| **Full Task CRUD** | Create, read, update, delete tasks with comments and labels |
| **Dashboard & Charts** | Interactive doughnut charts (Chart.js) showing task status and priority distribution |
| **PDF Export** | Generate a polished A4 PDF report with xhtml2pdf |
| **Async Architecture** | Celery + Redis handles heavy AI workloads without blocking the web server |
| **Docker Ready** | One-command production deployment with PostgreSQL, Redis, web, worker, and beat containers |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Runtime** | Python 3.13.13 |
| **Web Framework** | Flask 3.1.3 |
| **Frontend** | Jinja2 + HTMX 2.0.4 + Bootstrap 5.3.3 |
| **ORM** | Flask-SQLAlchemy 3.1.1 |
| **Migrations** | Flask-Migrate (Alembic) |
| **Auth** | Flask-Login 0.6.3 |
| **Forms** | Flask-WTF + WTForms |
| **AI** | OpenAI 2.37.0 |
| **Async Queue** | Celery 5.5.1 + Redis |
| **PDF** | xhtml2pdf 0.2.17 |
| **Charts** | Chart.js 4.4.7 |
| **Database** | SQLite (dev) / PostgreSQL 16 (prod) |
| **Container** | Docker + docker-compose |
| **WSGI** | gunicorn 23.0.0 |

---

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/mohammedrafeeq-dev/ai-task-manager.git
cd ai-task-manager
python -m venv venv
# Windows: venv\Scripts\activate  |  macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:
- `SECRET_KEY` — a random secret string
- `OPENAI_API_KEY` — your OpenAI API key (AI features require this)

### 3. Run

```bash
flask run
```

Open **http://localhost:5000** in your browser.

---

## Docker Deployment

Run the entire stack (web + worker + beat + PostgreSQL + Redis) with a single command:

```bash
docker-compose up --build
```

| Service | Role |
|---|---|
| `web` | Flask app behind gunicorn on port 5000 |
| `worker` | Celery worker consuming AI tasks |
| `beat` | Celery beat scheduling weekly reports |
| `db` | PostgreSQL 16 (persistent volume) |
| `redis` | Redis 7 message broker |

---

## Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=app --cov=core --cov=features --cov-report=html

# Open the HTML report
# Windows: start htmlcov/index.html
# macOS:   open htmlcov/index.html
```

**19 tests** passing across auth, organizations, tasks, dashboard, and PDF export.

---

## Project Structure

```
ai-task-manager/
├── app.py                  Flask application factory
├── celery_app.py           Celery app + beat schedule
├── config.py               Configuration classes
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
│
├── core/                   Application kernel
│   ├── database.py         SQLAlchemy instance
│   ├── extensions.py       Flask extension initialisation
│   ├── logging.py          Async non-blocking logger
│   ├── middleware.py       Request ID middleware
│   └── models/
│       └── mixins.py       PKMixin, TimestampMixin, OrganizationMixin
│
├── features/               Domain-driven modules
│   ├── auth/               Registration, login, logout
│   ├── organizations/      Multi-tenant org management
│   ├── tasks/              Full CRUD, comments, labels, PDF export
│   ├── ai/                 NLP parse, smart priority, chat, reports
│   └── dashboard/          Stats aggregation + Chart.js
│
├── templates/              Jinja2 templates
│   ├── base.html           Bootstrap 5 layout with nav
│   ├── auth/               Login & register pages
│   ├── organizations/      Create & settings pages
│   ├── tasks/              List, detail, form, PDF report
│   ├── dashboard/          Dashboard with Chart.js
│   └── ai/                 Chat interface
│
├── static/                 Static assets
│   ├── css/app.css         Custom styles
│   └── js/app.js           HTMX helpers & Chart.js
│
├── tests/                  19 passing tests
└── PROJECT_MAP.md          Full architecture reference
```

---

## API Endpoints

| Route | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/auth/login` | GET/POST | User login |
| `/auth/register` | GET/POST | User registration |
| `/auth/logout` | GET | Logout |
| `/org/create` | GET/POST | Create organization |
| `/org/settings` | GET/POST | Organization settings |
| `/tasks` | GET | Task list |
| `/tasks/new` | GET/POST | Create task |
| `/tasks/<id>` | GET | Task detail |
| `/tasks/<id>/edit` | GET/POST | Edit task |
| `/tasks/<id>/delete` | POST | Delete task |
| `/tasks/export/pdf` | GET | Export PDF report |
| `/dashboard` | GET | Dashboard with stats & charts |
| `/ai/parse` | POST | NLP task parsing |
| `/ai/suggest-priority` | POST | Priority suggestion |
| `/ai/chat` | GET/POST | AI chat assistant |

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | **Yes** | `dev-secret-key` | Flask session secret |
| `DATABASE_URL` | No | `sqlite:///data.db` | Database connection URI |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis broker URL |
| `OPENAI_API_KEY` | AI features | `""` | OpenAI API key |
| `FLASK_ENV` | No | `development` | `development` or `production` |

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using Flask, HTMX, and OpenAI
</p>
