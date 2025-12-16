FROM python:3.12.4-slim-bookworm

# Set working directory.
WORKDIR /code

# Copy dependencies.
COPY ./requirements.txt /code/requirements.txt

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 80

CMD ["fastapi", "run", "src/main.py", "--port", "80", "--host", "0.0.0.0"]
