FROM python:3.6.4-slim
LABEL Description="PubMed codethon deployment" Vendor="NLM" Version="0.0.1"

COPY gunicorn.config /gunicorn.config
COPY ./web_backend-0.0.tar.gz /web_backend-0.0.tar.gz



# ncbi-cloudblast-api is not in base.txt for app as we using it not via artifactory
RUN pip install --no-cache-dir  /web_backend-0.0.tar.gz && rm -rf /web_backend-0.0.tar.gz

CMD gunicorn --config /gunicorn.config web_backend:app