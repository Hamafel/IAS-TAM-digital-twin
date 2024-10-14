# Use the official Python 3.11 image
FROM python:3.11

WORKDIR /myapp

# Copy the requirements file into the container
COPY  ./requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the FastAPI application files to the /myapp directory
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
