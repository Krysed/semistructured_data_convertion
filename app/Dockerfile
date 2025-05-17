FROM python:alpine

WORKDIR /app

RUN apk add --no-cache curl py3-pip bash &&\ 
    pip install docker

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
