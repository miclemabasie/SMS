FROM python:3.12-slim

# Set environment variables
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/mediafiles
WORKDIR $APP_HOME

LABEL maintainer="miclemabasie3@gmail.com"
LABEL description="Development Image for SMS App"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
    build-essential libpq-dev gettext netcat-openbsd gcc postgresql curl python3-dev libffi-dev libssl-dev cargo \
    # WeasyPrint runtime deps
    libpango-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 shared-mime-info fonts-liberation \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


# Upgrade pip
RUN pip3 install --upgrade pip setuptools wheel \
    && pip3 install "multidict>=6.1.0" "aiohttp==3.9.1"

# Copy requirements and install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Set working directory where manage.py is located
WORKDIR $APP_HOME/src

# Setup entrypoint and start scripts
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

# setup entrypoint for celery
COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker && chmod +x /start-celeryworker

# setup entrypoint for flower
COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower && chmod +x /start-flower

# Set the entrypoint
ENTRYPOINT [ "/entrypoint" ]
