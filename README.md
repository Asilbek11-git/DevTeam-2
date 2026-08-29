# DevTeam - Modern SaaS Project & Task Management Platform

**DevTeam** is a production-ready, commercial multi-tenant SaaS platform built specifically for software engineering agencies, startups, tech teams, freelancers, and enterprise organizations.

---

## 🚀 Key Highlights & Architecture

- **Backend:** Python 3.12, Django 5.x, Django REST Framework, PostgreSQL, Redis, Celery & Celery Beat.
- **Frontend:** Server-Rendered Django Templates with Tailwind CSS, Vanilla JS, and asynchronous AJAX interactions.
- **Tenant Isolation:** Multi-tenant workspace architecture with row-level scoping and role-based access control (RBAC).
- **Agile Suite:** Interactive Kanban board with WIP limits, Sprints with Velocity and Burndown charts, Task Dependency Cycle prevention graph algorithm, live and manual Time Tracking with Billable tags.
- **VCS & Automations:** GitHub/GitLab/Bitbucket webhook ingestion (Commit -> Task activity, PR -> Code Review, Merge PR -> QA) and a customizable WHEN/THEN workflow automation engine.
- **SaaS Monetization:** Database-driven subscription tiers (Free, Pro, Business, Enterprise) with real-time limit enforcement, Multi-gateway payments (Stripe, Payme, Click), Invoicing, Promotional Coupons, Referral & Affiliate partner tracking.
- **SuperAdmin Business Suite:** Executive revenue dashboard featuring MRR, ARR, Churn, ARPU, Customer Health scores, and conversion funnel telemetry.
- **AI Intelligence:** Pluggable AI service (Google Gemini @google/genai) for auto-generating Acceptance Criteria, complexity estimation (story points/hours), release notes, and sprint retrospectives.
- **API Standards:** drf-spectacular OpenAPI 3.0, Swagger UI (`/api/docs/`), ReDoc (`/api/redoc/`), and standardized JSON envelope `{ success, message, data, errors }`.

---

## 🛠️ Quick Start with Docker Compose

```bash
# 1. Clone repository and setup environment
cp .env.example .env

# 2. Build and launch full Docker cluster (Django, PostgreSQL, Redis, Celery, Celery Beat)
docker-compose up --build -d

# 3. Access Web App on port 3000
# http://localhost:3000

# 4. OpenAPI Swagger UI documentation
# http://localhost:3000/api/docs/
```

---

## 🧪 Running Tests & Demo Data

```bash
# Seed realistic commercial demo data
python manage.py seed_demo

# Run comprehensive pytest test suite
pytest -v
```

---

## 💳 Payment Gateway Architecture

The billing system utilizes a strict Provider Abstraction pattern (`BasePaymentGateway`) allowing zero-downtime additions of payment processors:
- **Stripe:** International card payments and subscriptions with webhook signature verification.
- **Payme:** Central Asia / Uzbekistan JSON-RPC protocol with instant transaction clearing.
- **Click:** Merchant integration with MD5 token verification.
