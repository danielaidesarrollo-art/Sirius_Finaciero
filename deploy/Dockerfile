FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -t /app/site-packages

FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY --from=builder /app/site-packages /app/site-packages
COPY . /app

ENV PYTHONPATH=/app/site-packages
CMD ["main.py"]
