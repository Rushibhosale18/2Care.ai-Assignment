FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the python path so the seed script can find the modules
ENV PYTHONPATH=/app

# Initialize the clinical database
RUN python data/seed_db.py || echo "Seeding bypassed"

EXPOSE 8000

# Updated CMD for new directory structure
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
