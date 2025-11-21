
FROM python:3.15-rc-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/VishnuVardhanJS/Status-Logger .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
