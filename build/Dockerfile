FROM python:3.6.4-slim
LABEL Description="PubMed codethon deployment" Vendor="NLM" Version="0.0.1"

COPY gunicorn.config /gunicorn.config
COPY ./web_backend-0.0.tar.gz /web_backend-0.0.tar.gz
COPY keys.env /keys.env
COPY run_server.sh /run_server.sh

RUN pip install --no-cache-dir  /web_backend-0.0.tar.gz && rm -rf /web_backend-0.0.tar.gz

CMD /run_server.sh