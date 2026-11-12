FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (respects .gitignore)
COPY . .

# Run the Discord bot
CMD ["python", "bot.py"]
