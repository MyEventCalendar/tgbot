FROM python:3.10.4

COPY src/ /app/src/
COPY requirements.txt /app/
COPY entrypoint.sh /

RUN python3 -m pip install -r /app/requirements.txt && \
    chmod +x entrypoint.sh

ENTRYPOINT /entrypoint.sh
