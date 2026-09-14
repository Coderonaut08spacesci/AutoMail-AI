# 1. Base Image: Use a lightweight, official Python runtime
FROM python:3.11-slim

# 2. Work Directory: Create and set the folder inside the container where commands run
WORKDIR /app

# 3. Dependencies: Copy requirements first to leverage Docker's caching mechanism
COPY requirements.txt .

# 4. Install Dependencies: Install google-genai and python-dotenv inside the image
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Codebase: Copy all project files into the container
COPY . .

# 6. Default Command: The command Docker executes when the container starts
CMD ["python", "main.py"]

