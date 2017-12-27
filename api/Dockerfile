FROM python:3.5
LABEL J. Chaudourne <jchaudourne@laposte.net>

RUN groupadd docker && useradd -g docker api

ENV PYTHON_PIP_VERSION 9.0.1
RUN pip install --no-cache-dir --upgrade pip==$PYTHON_PIP_VERSION

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . /api

RUN chown -R api:docker /api/

USER api

EXPOSE 5500