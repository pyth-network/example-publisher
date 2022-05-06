FROM python:3.9.12-bullseye
RUN apt-get update && apt-get install -y supervisor

COPY . /publisher
WORKDIR /publisher

RUN python -m venv .venv
ENV PATH="/publisher/.venv/bin:$PATH"
RUN pip install --upgrade setuptools pip && pip install -e .

RUN ln -s supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
