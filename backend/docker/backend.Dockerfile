FROM python:3.10-slim

WORKDIR /app
COPY . /app

# install system deps for rasterio, gdal, etc. (simplified)
RUN apt-get update && \
    apt-get install -y build-essential gdal-bin libgdal-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r backend/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
