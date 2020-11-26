FROM python:3.8-slim-buster
ADD ./requirements.txt /app/requirements.txt

RUN set -ex \
    && apt-get update \
    && apt-get install -y python3-pip python3-dev libpq-dev curl build-essential python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info\
    && pip3 install virtualenv \
    && virtualenv env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

ADD . /app
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "myshop.wsgi:application"]
