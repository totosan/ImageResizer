FROM totosan/amd64-python:3.8-web-science
RUN apt- get update && apt- get install -y \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./app.py" ]
