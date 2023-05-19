FROM python:3.9.9-slim as base

CMD ["uvicorn", "app.main:app"]

EXPOSE 8080