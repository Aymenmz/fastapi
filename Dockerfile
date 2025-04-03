FROM python:3.12-slim

# Use environment variable for non-interactive apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install only required system packages and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure entrypoint is executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use unprivileged user (optional: add user in Dockerfile)
# RUN adduser --disabled-password appuser
# USER appuser

# Expose default port (optional if not handled via Kubernetes)
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
