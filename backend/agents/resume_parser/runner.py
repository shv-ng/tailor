import logging

from .graph import ResumeParserState, compiled_graph

logger = logging.getLogger(__name__)


def run_resume_parser(resume_text: str) -> ResumeParserState:
    initial_state = ResumeParserState(resume_text=resume_text)

    final_state = compiled_graph.invoke(initial_state)
    if final_state.get("error"):
        logger.error(final_state.get("error"))
    return ResumeParserState(**final_state)


if __name__ == "__main__":
    sample_markdown_resume = """
+917880795690 | shivangsrivastava157@gmail.com | Varanasi, Uttar Pradesh linkedin.com/in/shv-ng | github.com/shv-ng 

## **Shivang Srivastava** 

## **Summary** 

Backend developer with hands-on experience building production-grade Python services using FastAPI, PostgreSQL, and JWT-based authentication. Proficient in RESTful API design, asynchronous programming, database optimization, and containerized deployments with Docker. Strong foundation in system design with additional experience in Go for high-performance backend systems. 

## **Internship** 

**Backend Engineer Intern** Aug 2025 - Sep 2025 _JarNox Remote_ 

- Built and shipped a production **LLM-backed internal service** using **FastAPI** and **Redis** , enabling multiple engineers to consume AI-generated outputs reliably. 

- Optimized **PostgreSQL-backed APIs** by introducing **connection pooling** and query plan improvements, reducing production latency and improving throughput. 

- Implemented **role-based access control (RBAC)** middleware to safely expose AI-powered endpoints across internal services, enhancing security posture. 

## **Skills** 

**Languages:** Python, Go, SQL, Bash 

**Backend & APIs:** FastAPI, REST APIs, JWT, OAuth, gRPC, Go (net/http, Chi) **Databases & ORM:** PostgreSQL, SQLite, Redis, SQLAlchemy, SQLModel, Alembic **DevOps & Tooling:** Docker, Docker Compose, Git, Linux, CI/CD, PyTest **Problem Solving:** 400+ DSA problems solved; LeetCode rating 1678 

## **Projects** 

**ExpenseFlow: Expense Tracker** _| FastAPI, PostgreSQL, JWT, Alembic, Docker_ Live GitHub 

- Designed and built a full-stack expense tracking application with a FastAPI backend exposing **15+ RESTful endpoints** across 5 routers (auth, expenses, categories, analytics, users) with Pydantic request validation. 

- Implemented **JWT authentication** with Argon2 password hashing and managed relational schema across 3 tables (Users, Categories, Expenses) using SQLModel + Alembic migrations on PostgreSQL. 

- Delivered 3 analytics endpoints (daily, category, monthly spending breakdowns) and containerized the full stack with **Docker Compose** for reproducible one-command deployment. 

- **Stock Market Dashboard** _| FastAPI, scikit-learn, SQLite, slowapi, Docker_ Live GitHub 

- Built a FastAPI backend serving **65 stock tickers** across 3 REST endpoints — real-time prices, 1-year historical data, and 7-day price predictions using scikit-learn linear regression. 

- Implemented a **multi-layer caching system** (LRU cache with max size 128 + daily disk persistence) to minimize Yahoo Finance API calls, serving repeat queries from cache with no external network hop. 

- Added rate limiting via slowapi, SQLite-backed data persistence, and Dockerized the service with Docker Compose; frontend deployed live on Netlify. 

- **HireHustle: Job Application Tracker** _| Go (Chi), React, PostgreSQL, Docker_ Live Github 

- Built a REST API in Go with Chi, exposing 5 endpoints (full CRUD) for managing job applications across **10 workflow stages** modeled as a PostgreSQL enum type. 

- Used **sqlc** to generate type-safe Go code directly from SQL queries, with pgx/v5 as the driver — zero ORM overhead, no runtime SQL errors. 

- Containerized with Docker Compose and deployed on Vercel/Render; actively tracking **40+ real applications** with status transitions from wishlist to offer/rejection. 

## **Open Source Contribution** 

- **charmbracelet/bubbletea:** fix(examples): add missing WithWidth to table example (#1598). 

- **jackc/pgx:** Fixed empty `user=` override in PostgreSQL connection parsing that caused `SQLSTATE 28000` startup failures; aligned with libpq behavior (#2496). 

- **depado/quokka:** Fixed silent filesystem traversal failures by surfacing `filepath.Walk` permission errors in Analyze; added regression tests (#197). 

## **Education** 

**Veer Bahadur Singh Purvanchal University** 

Dec 2022 - May 2026 _Jaunpur, Uttar Pradesh_ 

_B.Tech in Computer Science and Engineering_ 

    """

    print("⏳ Running Resume Parser Agent...")
    result = run_resume_parser(sample_markdown_resume)

    import pprint

    pprint.pprint(result.parsed_resume)
