# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything into the container
COPY . /app

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run Streamlit dashboard
CMD ["streamlit", "run", "dashboard/streamlit_dashboard.py"]
