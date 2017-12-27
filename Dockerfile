FROM jupyter/base-notebook
LABEL J. Chaudourne <jchaudourne@laposte.net>

USER root
# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get install -yq --no-install-recommends \
    git \
    vim \
    build-essential \
    python-dev \
    unzip \
    libsm6 \
    pandoc \
    libxrender1 \
    && apt-get clean && \
rm -rf /var/lib/apt/lists/*

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 9.0.1
RUN pip install --no-cache-dir --upgrade pip==$PYTHON_PIP_VERSION

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# RUN chmod -r 777 ~/.local/share/jupyter

RUN jupyter contrib nbextension install
RUN jupyter nbextension enable codefolding/main

RUN mkdir -p /home/jovyan/.jupyter/migrated/
# RUN chmod -r 777 /home/jovyan/.jupyter/migrated
RUN locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LC_ALL fr_FR.UTF-8

# USER $NB_USER

WORKDIR "/notebooks"
