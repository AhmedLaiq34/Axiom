# Triggering fresh build 2026-03-09

FROM python:3.11-slim

# Force Python to print logs immediately so we aren't blind
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

# Add the 1000s timeout and set log level to info
CMD ["gunicorn", "-w", "1", "--timeout", "1000", "--log-level", "info", "-b", "0.0.0.0:7860", "server:app"]