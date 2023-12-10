# Use the official Python image as the base image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Install pt words
RUN python -m spacy download pt_core_news_sm

# Define as variáveis de ambiente necessárias para o debugpy
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the FastAPI application to run on
EXPOSE 8000

# Set the command to start the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]