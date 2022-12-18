FROM python:3.11
RUN apt update && apt install -y \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "./wsgi.py" ]
