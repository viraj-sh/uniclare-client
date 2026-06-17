FROM python:3.12-alpine AS builder

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt 

FROM python:3.12-alpine AS runner

COPY --from=builder /install /usr/local

ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

COPY ./app /app

CMD [ "fastapi", "run", "app/main.py", "--port", "80" ]

EXPOSE 80