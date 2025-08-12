FROM python:3.10-slim
LABEL authors="rudzc"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    YOLO_CONFIG_DIR=/app/.ultralytics

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libgl1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision numpy ultralytics

RUN awk 'BEGIN{IGNORECASE=1} !/^ *ultralytics([<=>~ ]|$)/' requirements.txt > /tmp/requirements-without-ultra.txt && \
    pip install --no-cache-dir -r /tmp/requirements-without-ultra.txt

COPY . .

# Listen on port 80 inside the container
EXPOSE 80

# Run gunicorn on port 80
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "-b", "0.0.0.0:80", "app:app"]
