# Jarvis CRM - Omnichannel Messaging Platform

## Prerequisites
- Docker & Docker Compose
- Python 3.12 (for local development outside Docker)

## Getting Started

1.  **Clone the repository** (or navigate to project root).

2.  **Environment Setup**
    The project comes with a default `.env` file configured for local Docker development.

3.  **Run with Docker**
    ```bash
    docker-compose up -d --build
    ```

    This will start:
    - **Backend API**: http://localhost:8000
    - **PostgreSQL**: Port 5432
    - **Redis**: Port 6379

4.  **Verify Status**
    Visit http://localhost:8000/docs to see the API documentation.
    Check health: http://localhost:8000/health

## Architecture
- **Framework**: FastAPI
- **Database**: PostgreSQL (Multi-tenant design)
- **Cache**: Redis
