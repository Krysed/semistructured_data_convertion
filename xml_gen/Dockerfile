FROM python:alpine

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/ 

EXPOSE 8001

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
