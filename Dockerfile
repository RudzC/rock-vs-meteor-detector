FROM python:3.10-slim
LABEL authors="rudzc"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    YOLO_CONFIG_DIR=/app/.ultralytics

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libgl1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
      torch==2.3.1

RUN awk 'BEGIN{IGNORECASE=1} !/^ *ultralytics([<=>~ ]|$)/' requirements.txt > /tmp/requirements-without-ultra.txt && \
    pip install --no-cache-dir -r /tmp/requirements-without-ultra.txt

RUN pip install --no-cache-dir --no-deps ultralytics==8.3.177

COPY . .

EXPOSE 4000
CMD ["gunicorn","-w","2","-k","gthread","--threads","4","-b","0.0.0.0:4000","app:app"]