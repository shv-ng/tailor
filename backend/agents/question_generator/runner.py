import logging

from agents.jd_analyzer.schemas import Job
from agents.resume_parser.schemas import Education, Experience, Link, Project, Resume

from .graph import QuestionGeneratorState, compiled_graph

logger = logging.getLogger(__name__)


def run_question_generator(
    parsed_resume: Resume, parsed_jd: Job
) -> QuestionGeneratorState:
    initial_state = QuestionGeneratorState(
        parsed_resume=parsed_resume, parsed_jd=parsed_jd
    )
    final_state = compiled_graph.invoke(initial_state)
    if final_state.get("error"):
        logger.error(final_state.get("error"))
    return QuestionGeneratorState(**final_state)


if __name__ == "__main__":
    parsed_resume_obj = Resume(
        name="Shivang Srivastava",
        email="shivangsrivastava157@gmail.com",
        phone="+917880795690",
        location="Varanasi, Uttar Pradesh",
        summary="Backend developer with hands-on experience building production-grade Python services using FastAPI, PostgreSQL, and JWT-based authentication. Proficient in RESTful API design, asynchronous programming, database optimization, and containerized deployments with Docker. Strong foundation in system design with additional experience in Go for high-performance backend systems.",
        links=[
            Link(label="LinkedIn", url="linkedin.com/in/shv-ng"),
            Link(label="GitHub", url="github.com/shv-ng"),
        ],
        skills={
            "Languages": ["Python", "Go", "SQL", "Bash"],
            "Backend & APIs": [
                "FastAPI",
                "REST APIs",
                "JWT",
                "OAuth",
                "gRPC",
                "Go (net/http, Chi)",
            ],
            "Databases & ORM": [
                "PostgreSQL",
                "SQLite",
                "Redis",
                "SQLAlchemy",
                "SQLModel",
                "Alembic",
            ],
            "DevOps & Tooling": [
                "Docker",
                "Docker Compose",
                "Git",
                "Linux",
                "CI/CD",
                "PyTest",
            ],
            "Problem Solving": ["400+ DSA problems solved", "LeetCode rating 1678"],
        },
        experiences=[
            Experience(
                company="JarNox",
                role="Backend Engineer Intern",
                employment_type="Internship",
                location="Remote",
                start_date="Aug 2025",
                end_date="Sep 2025",
                duration=None,
                summary=[
                    "Built and shipped a production LLM-backed internal service using FastAPI and Redis, enabling multiple engineers to consume AI-generated outputs reliably.",
                    "Optimized PostgreSQL-backed APIs by introducing connection pooling and query plan improvements, reducing production latency and improving throughput.",
                    "Implemented role-based access control (RBAC) middleware to safely expose AI-powered endpoints across internal services, enhancing security posture.",
                ],
                technologies=["FastAPI", "Redis", "PostgreSQL"],
            )
        ],
        projects=[
            Project(
                name="ExpenseFlow: Expense Tracker",
                description=[
                    "Designed and built a full-stack expense tracking application with a FastAPI backend exposing 15+ RESTful endpoints across 5 routers (auth, expenses, categories, analytics, users) with Pydantic request validation.",
                    "Implemented JWT authentication with Argon2 password hashing and managed relational schema across 3 tables (Users, Categories, Expenses) using SQLModel + Alembic migrations on PostgreSQL.",
                    "Delivered 3 analytics endpoints (daily, category, monthly spending breakdowns) and containerized the full stack with Docker Compose for reproducible one-command deployment.",
                ],
                technologies=["FastAPI", "PostgreSQL", "JWT", "Alembic", "Docker"],
                github_url=None,
                live_url=None,
            ),
            Project(
                name="Stock Market Dashboard",
                description=[
                    "Built a FastAPI backend serving 65 stock tickers across 3 REST endpoints — real-time prices, 1-year historical data, and 7-day price predictions using scikit-learn linear regression.",
                    "Implemented a multi-layer caching system (LRU cache with max size 128 + daily disk persistence) to minimize Yahoo Finance API calls, serving repeat queries from cache with no external network hop.",
                    "Added rate limiting via slowapi, SQLite-backed data persistence, and Dockerized the service with Docker Compose; frontend deployed live on Netlify.",
                ],
                technologies=["FastAPI", "scikit-learn", "SQLite", "slowapi", "Docker"],
                github_url=None,
                live_url=None,
            ),
            Project(
                name="HireHustle: Job Application Tracker",
                description=[
                    "Built a REST API in Go with Chi, exposing 5 endpoints (full CRUD) for managing job applications across 10 workflow stages modeled as a PostgreSQL enum type.",
                    "Used sqlc to generate type-safe Go code directly from SQL queries, with pgx/v5 as the driver — zero ORM overhead, no runtime SQL errors.",
                    "Containerized with Docker Compose and deployed on Vercel/Render; actively tracking 40+ real applications with status transitions from wishlist to offer/rejection.",
                ],
                technologies=["Go (Chi)", "React", "PostgreSQL", "Docker"],
                github_url=None,
                live_url=None,
            ),
        ],
        education=[
            Education(
                institution="Veer Bahadur Singh Purvanchal University",
                degree="B.Tech in Computer Science and Engineering",
                field_of_study=None,
                location="Jaunpur, Uttar Pradesh",
                start_date="Dec 2022",
                end_date="May 2026",
            )
        ],
        open_source_contributions=[
            "charmbracelet/bubbletea: fix(examples): add missing WithWidth to table example (#1598).",
            "jackc/pgx: Fixed empty user= override in PostgreSQL connection parsing that caused SQLSTATE 28000 startup failures; aligned with libpq behavior (#2496).",
            "depado/quokka: Fixed silent filesystem traversal failures by surfacing filepath.Walk permission errors in Analyze; added regression tests (#197).",
        ],
    )
    parsed_jd_obj = Job(
        role="Open Source Contributor",
        company="OrcaRouter",
        required_skills=[
            "LLM routing",
            "Systems programming",
            "Performance optimization",
            "API development",
            "Inference optimization",
        ],
        preferred_skills=[
            "Embeddings",
            "Bandit algorithms",
            "Heuristics",
            "Cache invalidation",
            "Batching",
            "KV-cache routing",
            "Reward modeling",
        ],
        experience_required="Not specified",
        responsibilities=[
            "Develop LLM routing models balancing cost, quality, and latency",
            "Implement adaptive routing using embeddings and heuristics",
            "Build deterministic prompt caching systems",
            "Optimize inference through batching and streaming",
            "Integrate various AI providers including OpenAI, Anthropic, and Gemini",
            "Maintain an OpenAI-compatible API layer",
            "Improve developer experience through SDKs and CLI tools",
        ],
        keywords=[
            "LLM",
            "AI inference",
            "Open Source",
            "Routing",
            "Caching",
            "Latency",
            "Throughput",
            "OpenAI",
            "Anthropic",
            "Gemini",
            "Groq",
            "SDK",
            "CLI",
        ],
    )
    print("⏳ Running Questions Generator Agent...")
    analysis_result = run_question_generator(
        parsed_resume=parsed_resume_obj, parsed_jd=parsed_jd_obj
    )
    import pprint

    pprint.pprint(analysis_result.questions)
