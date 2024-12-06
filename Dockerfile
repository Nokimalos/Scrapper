FROM python:3.9-slim

ARG URL
ARG WEBHOOK_URL

WORKDIR /app

RUN echo "URL=$URL" >> .env && \
    echo "WEBHOOK_URL=$WEBHOOK_URL" >> .env

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY article_notifier.py .

CMD ["python", "article_notifier.py"]
