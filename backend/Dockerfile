FROM python:3.12-slim
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy rest of code
COPY . .

EXPOSE 8000
