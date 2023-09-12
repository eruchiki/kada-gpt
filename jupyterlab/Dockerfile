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
