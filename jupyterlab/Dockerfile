FROM python:3.11.5-bookworm
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tzdata jq \
&&  ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Tokyo

RUN python3 -m pip install --upgrade pip \
&&  pip install --no-cache-dir \
    jupyterlab \
    jupyterlab-language-pack-ja-jp \
    black \
    jupyterlab_code_formatter \
    jupyterlab-git \
    jupyterlab_widgets \
    ipywidgets \
    import-ipynb

RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    matplotlib \
    seaborn \
    requests \
    beautifulsoup4 \
    Pillow \
    opencv-python \
    llama-index \
    nltk \
    pypdf \
    pdfminer.six \
    chromadb