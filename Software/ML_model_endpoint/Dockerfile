# Use the official Python 3.11 image
FROM python:3.11-slim



# Set the working directory inside the container
WORKDIR /myapp

# Copy the requirements file into the container
COPY --chown=user ./requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the FastAPI application files to the /myapp directory
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
