FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/.

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model.pkl file into the container
COPY model.pkl /app/

# Copy the main.py file into the container
COPY main.py /app/

# Expose the port that FastAPI will run on (change as needed)
EXPOSE 8082

# Command to run the FastAPI application within the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]
