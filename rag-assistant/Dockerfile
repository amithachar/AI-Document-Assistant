# -------- Builder --------
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# -------- Runtime --------
FROM python:3.10-slim

WORKDIR /app

RUN useradd -m -u 1001 -s /usr/sbin/nologin appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]