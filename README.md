
Run backend with this command

```py
uv run uvicorn app.main:app --reload
```

Docker build and run commands

```bash
docker build -t celesta-backend:latest .
docker run -p 8000:80 --name celesta-backend celesta-backend:latest
```
