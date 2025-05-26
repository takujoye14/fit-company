FROM python:3.13

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv pip install --system --project . --editable .

COPY . .

EXPOSE 5001

CMD ["python", "main.py"]