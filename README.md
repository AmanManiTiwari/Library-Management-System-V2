<div align="center">

# 📚 Library Management System V2

**A full-stack, decoupled library management platform — Vue 3 SPA frontend, Flask + JWT REST API backend, with async email notifications and scheduled reporting via Celery + Redis.**

[![Python](https://img.shields.io/badge/Python-3.10%2F3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Celery](https://img.shields.io/badge/Celery-Async%20Tasks-37814A?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-Broker%20%2F%20Cache-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

[Overview](#-overview) •
[Features](#-features) •
[Architecture](#-architecture) •
[Tech Stack](#-tech-stack) •
[Getting Started](#-getting-started) •
[API Reference](#-api-reference) •
[Background Jobs](#-background-jobs) •
[Project Structure](#-project-structure)

</div>

---

## 📖 Overview

**Library Management System V2** is a ground-up rebuild of the original [Library Management System](https://github.com/AmanManiTiwari/Library-Management-System-V1), evolving it from a monolithic Flask + Jinja2 app into a **decoupled architecture**: a **Vue 3 single-page application** frontend talking to a **stateless, JWT-authenticated Flask REST API** backend.

The backend also introduces an **asynchronous task pipeline** powered by **Celery** and **Redis**, handling scheduled email reminders, monthly usage reports, and on-demand CSV report generation/export — capabilities that didn't exist in V1.

As with V1, the system supports two roles — **Librarians** (admins) and **Members** — with catalog browsing, book requests, issuing/returning, feedback, and usage analytics via generated charts.

---

## ✨ What's New Since V1

| Area | V1 | V2 |
|---|---|---|
| Frontend | Server-rendered Jinja2 templates | Decoupled **Vue 3** SPA (Vue Router) |
| API | Flask-RESTful, session-based | Pure JSON REST API secured with **JWT** (`flask-jwt-extended`) |
| Passwords | Plain text | **Hashed with Bcrypt** (`flask-bcrypt`) |
| Serialization | Manual dicts / `marshal_with` | **Flask-Marshmallow** schemas |
| Background work | None (synchronous only) | **Celery** workers + **Redis** broker/backend for async jobs |
| Notifications | None | Automated email via **Flask-Mail** (daily inactivity reminders, monthly reports) |
| Reporting | Live Matplotlib chart, in-page | On-demand bar/pie charts **and** async **CSV export with email delivery** |
| Caching | None | **Flask-Caching** with Redis backend |

---

## ✨ Features

### 👩‍💼 Librarian (Admin)
- Full CRUD on **sections** and **books**
- Review, **accept**, or **reject** member book requests
- View and **revoke** currently issued books
- Visual analytics: **issued-books bar chart** and **issues-by-section pie chart**
- **Export all issue records to CSV** as a background job, delivered via email with a download link
- Auto-generated monthly **email reports** per member summarizing books issued

### 🙋 Member (User)
- Register and log in (JWT-based session)
- Browse the catalog by section, view book details
- **Request** a book from the librarian
- View and **return** currently issued books
- Submit **feedback** on a book
- Receive an automated **"we miss you" email** after 24 hours of inactivity

### ⚙️ Platform
- Stateless **JWT authentication** — no server-side sessions
- **Role-based authorization** enforced per-endpoint (`is_librarian` checks)
- **Async task queue** (Celery + Redis) for anything that shouldn't block a request: emails, scheduled reports, CSV exports
- **MailHog**-compatible local SMTP setup for testing outbound email without a real mail server
- **Response caching** (Flask-Caching + Redis) for expensive read endpoints

---

## 🏗 Architecture

```
┌─────────────────────┐        JWT-authenticated REST/JSON        ┌──────────────────────────┐
│   Vue 3 SPA          │ ─────────────────────────────────────▶  │   Flask REST API          │
│  (frontend/, :8080)  │ ◀─────────────────────────────────────  │  (bakend/app.py, :5000)   │
└─────────────────────┘                                           └────────────┬─────────────┘
                                                                                 │
                                          ┌──────────────────────────────────────┼───────────────────────┐
                                          ▼                                      ▼                        ▼
                                 ┌─────────────────┐               ┌────────────────────────┐   ┌────────────────┐
                                 │ SQLite (SQLAlchemy)│             │  Celery worker + beat   │   │  Redis          │
                                 │ Users/Books/Issues  │            │  (task.py, workers.py)  │   │ broker · cache  │
                                 └─────────────────┘               └───────────┬─────────────┘   └────────────────┘
                                                                                 ▼
                                                                     ┌────────────────────┐
                                                                     │ MailHog / SMTP      │
                                                                     │ (Flask-Mail)        │
                                                                     └────────────────────┘
```

- **Frontend** — Vue 3 + Vue Router SPA that consumes the REST API directly (folder: `frontend/`)
- **API layer** — Flask app exposing JSON endpoints, protected with JWT (folder: `bakend/`)
- **Persistence** — SQLite via SQLAlchemy ORM, with Marshmallow schemas for serialization
- **Async layer** — Celery workers process scheduled and on-demand jobs (reminders, reports, CSV export), backed by Redis as both broker and result store
- **Email** — Flask-Mail sends HTML emails (rendered from Jinja templates) through a local SMTP relay such as MailHog during development

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vue 3, Vue Router, Vue CLI |
| **Backend / API** | Python, Flask, Flask-CORS |
| **Auth** | Flask-JWT-Extended, Flask-Bcrypt |
| **ORM / Serialization** | Flask-SQLAlchemy, SQLAlchemy, Flask-Marshmallow |
| **Database** | SQLite |
| **Async Tasks / Scheduling** | Celery (worker + beat), Redis (broker & result backend) |
| **Caching** | Flask-Caching (Redis backend) |
| **Email** | Flask-Mail, MailHog (dev SMTP) |
| **Charts / Reporting** | Matplotlib, CSV export |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js + npm (for the Vue frontend)
- [Redis](https://redis.io/docs/getting-started/) server
- [MailHog](https://github.com/mailhog/MailHog) (or any local SMTP catcher) for testing emails

### 1. Backend setup

```bash
git clone https://github.com/AmanManiTiwari/Library-Management-System-V2.git
cd "Library-Management-System-V2/bakend"

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Frontend setup

```bash
cd ../frontend
npm install
```

### 3. Run all services

The project needs several processes running concurrently — a repository-provided reference (`command to run file.txt`) lists them:

```bash
# Terminal 1 — Flask API
cd bakend && python3 app.py

# Terminal 2 — Redis (broker + cache)
redis-server

# Terminal 3 — MailHog (local SMTP + web UI, default at http://localhost:8025)
MailHog

# Terminal 4 — Celery worker
cd bakend && celery -A app.celery worker --loglevel=INFO

# Terminal 5 — Celery beat (scheduler, for periodic reminders/reports)
cd bakend && celery -A app.celery beat --max-interval 1 -l info

# Terminal 6 — Vue frontend
cd frontend && npm run serve
```

- Backend API: **http://127.0.0.1:5000**
- Frontend SPA: **http://localhost:8080**

On first run, the SQLite database and tables are created automatically, along with a default librarian account.

### Default Librarian Login

| Field | Value |
|---|---|
| Email | `admin@gmail.com` |
| Password | `0` |


---

## 📡 API Reference

All endpoints return JSON. Endpoints marked 🔒 require a valid JWT (`Authorization: Bearer <token>`), obtained from `/userlogin`.

### Auth
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/userregister` | Register a new member |
| `POST` | `/userlogin` | Log in, returns a JWT access token |
| `GET` | `/protected` 🔒 | Verify a token / fetch identity |
| `POST` | `/logout` 🔒 | Clear JWT cookie |
| `GET` | `/getuserinfo` | Fetch current user info |

### Sections
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/sections` | List all sections with book counts |
| `GET` | `/section/<id>` | Get a section by ID |
| `POST` | `/section/add` 🔒 | Create a section *(librarian only)* |
| `PUT` | `/section/update/<id>` 🔒 | Update a section *(librarian only)* |
| `DELETE` | `/section/delete/<id>` 🔒 | Delete a section *(librarian only)* |
| `GET` | `/section/<id>/book` | List books in a section |

### Books
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/books` | List all books |
| `GET` | `/book/<id>` | Get a book by ID |
| `POST` | `/section/<id>/book/add` 🔒 | Add a book to a section *(librarian only)* |
| `PUT` | `/book/update/<id>` 🔒 | Update a book *(librarian only)* |
| `DELETE` | `/book/<id>` 🔒 | Delete a book *(librarian only)* |
| `GET` | `/getallbookinfo` | Fetch full details for all books |

### Requests, Issues & Feedback
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/bookrequested` | List all pending requests |
| `POST` | `/accept/<id>` | Approve a request → creates an Issue |
| `DELETE` | `/reject/<id>` | Reject a request |
| `GET` | `/bookstatus` | List all currently issued books |
| `DELETE` | `/revoke/<id>` | Librarian revokes an issued book |
| `POST` | `/request/<id>` 🔒 | Member requests a book |
| `GET` | `/issued` 🔒 | Member's currently issued books |
| `DELETE` | `/return/<id>` 🔒 | Member returns a book |
| `POST` | `/submitFeedback` 🔒 | Submit feedback on a book |

### Reporting & Export
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/book-issued-history-report` | JSON counts: sections, books, requests, issues |
| `GET` | `/stats` | PNG bar chart of library activity |
| `GET` | `/issue-section-pie-chart` | PNG pie chart of issues by section |
| `GET` | `/export_csv_report` | Kicks off an **async** Celery job to build a CSV report and email a download link |
| `GET` | `/download/<filename>` | Download a generated CSV report |

---

## ⏱ Background Jobs

Scheduled and on-demand work runs on **Celery**, using **Redis** as both broker and result backend:

- **`daily_reminder`** — runs periodically; emails members who haven't logged in for 24+ hours
- **`monthly_report`** — runs periodically; emails each member a summary of books they've issued in the last 30 days
- **`export_csv`** — triggered on demand via `/export_csv_report`; generates a CSV of all issue records and emails the librarian a download link

> 📝 In the current codebase both periodic tasks are scheduled with `crontab(minute="*/1")` (every minute) for development/demo purposes — the intended production schedules (daily at a fixed hour, monthly on the 1st) are present in code as comments and should be enabled before deployment.

---

## 🗂 Project Structure

```
Library-Management-System-V2/
├── command to run file.txt         # Reference commands to start all services
├── bakend/                         # Flask REST API
│   ├── app.py                      # Routes, JWT auth, charts, CSV export trigger
│   ├── config.py                   # App configuration (DB, JWT, Celery, Mail, Cache)
│   ├── models.py                   # SQLAlchemy models + Marshmallow schemas
│   ├── mailer.py                   # Email-sending helper
│   ├── task.py                     # Celery tasks (reminders, reports, CSV export)
│   ├── workers.py                  # Celery app instance + Flask app-context task base
│   ├── requirements.txt
│   ├── instance/lmsv2.db           # SQLite database (auto-generated)
│   ├── exports/                    # Generated CSV reports
│   └── templates/                  # HTML email templates (daily.html, monthly_report.html)
└── frontend/                       # Vue 3 SPA
    ├── package.json
    ├── src/
    │   ├── App.vue, main.js
    │   ├── router/index.js         # Vue Router routes
    │   ├── mixins/userMixin.js     # Shared auth/user logic
    │   ├── components/NavBar.vue
    │   └── views/                  # Login, Register, Sections, Books, Requests, Stats, etc.
    └── public/
```

### Data Model

```
User ─┬─< Issues >─┬─ Book ─┬─< Section
      ├─< Request  >┘        │
      └─< Feedback           │
Feedback ── User, Book
```

- **User** — email, hashed password, name, `is_librarian` flag, `latest_loggedin` (drives inactivity reminders)
- **Section** — a category grouping books
- **Book** — belongs to a Section
- **Request** — a member's pending request for a Book
- **Issues** — a Book currently checked out to a User, with issue `date`
- **Feedback** — a member's comment on a Book

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project currently has no explicit license file. Consider adding an [MIT License](https://choosealicense.com/licenses/mit/) to clarify usage rights for contributors and users.

---

## 👤 Author

**Aman Mani Tiwari**
GitHub: [@AmanManiTiwari](https://github.com/AmanManiTiwari)

<div align="center">

If you found this project useful, consider giving it a ⭐!

</div>
