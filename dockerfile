FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY apps/ .
CMD ["gunicorn", "root.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "3"]