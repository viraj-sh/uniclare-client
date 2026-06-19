FROM python:3.12-alpine AS backend_builder

WORKDIR /app

RUN apk add --no-cache nodejs npm && \
    node -v && npm -v

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

WORKDIR /app/frontend
RUN npm install && npm run build

FROM python:3.12-alpine AS runner

COPY --from=backend_builder /install /usr/local
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /app

COPY --from=backend_builder /app/backend/app .

CMD ["fastapi", "run", "main.py", "--port", "80"]

EXPOSE 80