# Dockerfile — ACEest Fitness & Gym
# =============================================================================
# WHY python:3.11-slim?
#   - "slim" = stripped-down Debian base, ~150MB vs ~900MB for full Python image
#   - Smaller image = faster CI/CD pulls, less attack surface, better security
# =============================================================================
FROM python:3.11-slim

# =============================================================================
# SECURITY: Create a non-root user
# Running as root inside a container is a security risk.
# If the app is compromised, attacker only gets "appuser" privileges, not root.
# =============================================================================
RUN adduser --disabled-password --gecos "" appuser

# =============================================================================
# WORKDIR: All subsequent commands run from /app inside the container
# =============================================================================
WORKDIR /app

# =============================================================================
# LAYER CACHING OPTIMIZATION:
# Copy requirements.txt FIRST (before the rest of the code).
# Docker caches each layer. If only app.py changes, the pip install layer
# is reused from cache — making rebuilds much faster.
# =============================================================================
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Copy the rest of the project into the container
# =============================================================================
COPY . .

# =============================================================================
# Switch to the non-root user AFTER installing packages (pip needs root)
# =============================================================================
USER appuser

# =============================================================================
# Tell Docker this container listens on port 5000
# (This is documentation — actual port mapping happens in `docker run -p`)
# =============================================================================
EXPOSE 5000

# =============================================================================
# CMD: The command that runs when the container starts
# Using "python app.py" keeps it simple and visible in CI logs
# =============================================================================
CMD ["python", "app.py"]
