FROM python:3.10-slim
LABEL authors="rudzc"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV YOLO_CONFIG_DIR=/app/.ultralytics
RUN mkdir -p /app/.ultralytics

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libgl1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir torch==2.3.1 --index-url https://download.pytorch.org/whl/cpu

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r <(grep -v 'torch' requirements.txt)

COPY . .

EXPOSE 4000

CMD ["gunicorn","-w","2","-k","gthread","--threads","4","-b","0.0.0.0:4000","app:app"]