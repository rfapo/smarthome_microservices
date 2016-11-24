FROM resin/rpi-raspbian:wheezy

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-virtualenv \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pymongo

RUN pip install paho-mqtt

COPY ./app /app

WORKDIR /app

CMD ["python", "./mqtt-client-v2.py"]
