<p align="center">
  <img src="./assets/Logo_Dark.svg" he alt="Celeste Logo" />
</p>

<div align="center">
    <h1>【 Celeste Backend 】</h1>
    <h3></h3>
</div>

<div align="center">

![](https://img.shields.io/github/last-commit/Rnbsov/celeste-backend?&style=for-the-badge&color=FFB1C8&logoColor=D9E0EE&labelColor=292324)
![](https://img.shields.io/github/stars/Rnbsov/celeste?style=for-the-badge&logo=andela&color=FFB686&logoColor=D9E0EE&labelColor=292324)
[![](https://img.shields.io/github/repo-size/Rnbsov/celeste-backend?color=CAC992&label=SIZE&logo=googledrive&style=for-the-badge&logoColor=D9E0EE&labelColor=292324)](https://github.com/Rnbsov/hyprland)
![](https://img.shields.io/badge/issues-skill-green?style=for-the-badge&color=CCE8E9&logoColor=D9E0EE&labelColor=292324)

</div>

<div align="center">
    <h2>• overview •</h2>
    <h3></h3>
</div>

## About Celeste Backend

This is the backend service powering the [Celeste microgreens tracking app](https://github.com/Rnbsov/celeste). Built with FastAPI, it provides a robust API for managing microgreens batches, phenological records, growth tracking, and user management.

## Key Features

### 🌱 Data Management API
- CRUD operations for microgreens batches
- Growth journal entry management
- Secure user authentication and authorization
- Analytics and statistics endpoints

### ⚡ High Performance
- Asynchronous request handling with FastAPI
- DragonFlyDB caching for high-throughput operations
- Containerized deployment for scalability

### 📊 Documentation
- Auto-generated OpenAPI documentation
- Interactive API testing with Swagger UI alternative (Scalar API)
- Comprehensive endpoint descriptions

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Caching**: [DragonFlyDB](https://www.dragonflydb.io/) (modern Redis alternative)
- **Authentication**: JWT with OAuth2
- **Containerization**: Docker
- **Documentation**: OpenAPI with Scalar API UI

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Rnbsov/celeste-backend.git
   cd celeste-backend
   ```
2. Install uv and run:
    ```bash
    uv venv
    uv add
    ```
3. Setup environment variables (create a `.env` file based on `.env.example`)
4. Run backend with this command
    ```py
    uv run uvicorn app.main:app --reload
    ```

## Docker

Docker build and run commands

```bash
docker build -t celesta-backend:latest .
docker run -p 8000:80 --name celesta-backend celesta-backend:latest
```
