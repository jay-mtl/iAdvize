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

RUN  apt-get clean && apt-get update && apt-get install -y locales

# Change the locale to Fr to use it in the date parsing
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG fr_FR.UTF-8  
ENV LC_ALL fr_FR.UTF-8

USER api

EXPOSE 5500