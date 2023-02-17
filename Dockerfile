FROM python:3.9.12-bullseye

COPY . /publisher
WORKDIR /publisher

RUN pip install --upgrade setuptools pip && pip install -e .

CMD ["python", "-m", "publisher", "--config", "config/config.toml"]
