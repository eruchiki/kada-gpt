FROM python:3.11.5-bookworm
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tzdata jq \
&&  ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Tokyo
COPY requirements.txt /root/
RUN python3 -m pip install --upgrade pip \
&&  pip install --no-cache-dir -r /root/requirements.txt \
&&  rm -f /root/requirements.txt

# Neologd
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y mecab && \
    apt-get install -y libmecab-dev && \
    apt-get install -y mecab-ipadic-utf8 && \
    apt-get install -y git && \
    apt-get install -y make && \
    apt-get install -y curl && \
    apt-get install -y xz-utils && \
    apt-get install -y file && \
    apt-get install -y sudo
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
  cd mecab-ipadic-neologd && \
  ./bin/install-mecab-ipadic-neologd -n -y && \
  echo dicdir = `mecab-config --dicdir`"/mecab-ipadic-neologd">/etc/mecabrc && \
  sudo cp /etc/mecabrc /usr/local/etc && \
  cd ..