# PROJECT_MAP: AI-Powered Task Management (Flask SaaS)

> Last updated: 2026-05-16 | Python 3.13.13 | 19/19 tests passing | 72% coverage

---

## [TECH_STACK]

| Layer | Technology | Version |
|---|---|---|
| Runtime | Python | 3.13.13 |
| Web Framework | Flask | 3.1.3 |
| Frontend | Jinja2 + HTMX | 2.0.4 |
| ORM | Flask-SQLAlchemy | 3.1.1 |
| Migrations | Flask-Migrate (Alembic) | 4.1.0 |
| Auth | Flask-Login | 0.6.3 |
| Forms | Flask-WTF + WTForms | 1.2.2 |
| AI | openai | 2.37.0 |
| Async Queue | Celery | 5.5.1 |
| Broker | Redis | 5.3.1 (client) |
| Config | python-dotenv | 1.2.2 |
| WSGI | gunicorn | 23.0.0 |
| Testing | pytest + pytest-cov | 8.3.5 |
| CSS | Bootstrap 5 | 5.3.3 |
| PDF Generation | xhtml2pdf | 0.2.17 |
| Charts | Chart.js | 4.4.7 |
| Container | Docker + docker-compose | — |

---

## [SYSTEM_FLOW]

```
Browser (HTMX) ──HTTP──> Flask App ──> SQLAlchemy (SQLite/PostgreSQL)
                            │
                            ├──> OpenAI API (sync chat/nlp)
                            │
                            └──> Celery Worker ──> Redis
                                    └── generate_weekly_reports
```

### Blueprint Routes

| Prefix | Blueprint | Key Endpoints |
|---|---|---|
| `/auth` | auth | login, register, logout |
| `/org` | organizations | create, settings |
| `/tasks` | tasks | list, new, view, edit, delete, export/pdf |
| `/ai` | ai | chat, parse, suggest-priority |
| `/dashboard` | dashboard | index (stats) |
| `/health` | — | health check |

---

## [ARCHITECTURE]

```
ai-task-manager/
├── app.py                    # Flask factory + entry
├── celery_app.py             # Celery + beat schedule
├── config.py                 # Config, DevConfig, ProdConfig
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .env.example
├── .gitignore
│
├── core/                     # Shared kernel
│   ├── database.py           # SQLAlchemy instance
│   ├── extensions.py         # Flask extension init
│   ├── logging.py            # AsyncQueueHandler
│   ├── middleware.py         # Request ID
│   └── models/mixins.py      # PKMixin, TimestampMixin, OrganizationMixin
│
├── features/                 # Domain-driven modules
│   ├── auth/                 # routes, models (User), forms
│   ├── organizations/        # routes, models (Organization), forms
│   ├── tasks/                # routes, models (Task, TaskComment, TaskLabel), forms
│   ├── ai/                   # routes, models (AIInteraction), services/, tasks.py
│   └── dashboard/            # routes (stats aggregation)
│
├── templates/                # Jinja2 (one subdir per feature)
├── static/                   # CSS, JS
├── tests/                    # 18 tests across 3 modules
└── PROJECT_MAP.md
```

---

## [SAFE_LOGGING] — AsyncQueueHandler

- **Non-blocking**: `queue.Queue` + daemon thread
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Output**: Rotating file `logs/app.log` (10MB x 5)
- **Request ID**: UUID hex per request injected into `g`
- **AI Audit**: All OpenAI calls logged to `AIInteraction` table

---

## [ORPHANS & PENDING]

| Item | Status | Notes |
|---|---|---|
| Celery worker auto-start in docker | ✅ Done | Defined in docker-compose |
| Celery task retry + backoff | ✅ Done | max_retries=3, delay=60s |
| HTMX loading indicators | ✅ Done | JS auto-scroll for chat |
| File attachments on tasks | ❌ Not in scope | Orphan — not requested |
| Email notifications | ❌ Not in scope | Orphan — not requested |
| Organization invite flow | ❌ Not in scope | Orphan — not requested |
| PDF export button on task list | ✅ Done | `/tasks/export/pdf` route + service + test |
| Dashboard Chart.js visualizations | ✅ Done | Doughnut charts for status + priority |
| Task list badges & improved UI | ✅ Done | Bootstrap badges for status/priority |
| AI route rate limiting | ⏳ PENDING | Per-user limits via middleware |
| Alembic migration setup | ⏳ PENDING | Flask-Migrate initted; run `flask db init` |
| Production README | ⏳ PENDING | Basic setup instructions |
| Static cache busting | ⏳ PENDING | For production optimization |
| AI service unit tests | ⏳ PENDING | Requires OPENAI_API_KEY or mock |

---

## [MILESTONES STATUS]

| # | Milestone | Status | Verification |
|---|---|---|---|
| M1 | Skeleton + Core | ✅ Done | `flask run` starts, /health 200 |
| M2 | Auth | ✅ Done | 7 tests pass |
| M3 | Organizations | ✅ Done | 3 tests pass |
| M4 | Tasks CRUD | ✅ Done | 7 tests pass |
| M5 | Dashboard | ✅ Done | 1 test passes |
| M6 | AI: NLP Parse | ✅ Done | Service written, route registered |
| M7 | AI: Priority | ✅ Done | Service written, route registered |
| M8 | AI: Chat | ✅ Done | Streaming endpoint registered |
| M9 | AI: Reports | ✅ Done | Celery task + beat schedule |
| M10 | Tests + Coverage | ✅ Done | 19 tests, 72% coverage |
| M12 | UI Polish + PDF Export | ✅ Done | Chart.js dashboard, badges, PDF report export |
| M11 | Docker + Deploy | ✅ Done | Dockerfile + docker-compose |
