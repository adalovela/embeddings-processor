FROM python:3.10

RUN groupadd --gid 1000 app && \
    useradd --create-home --gid 1000 --uid 1000 app

COPY ./email-embeddings-processor/requirements.txt email-embeddings-processor/service/requirements.txt
ADD ./email-embeddings-processor email-embeddings-processor/service
ADD ./email-embeddings-processor email-embeddings-processor/config
WORKDIR email-embeddings-processor/service

ENV FLASK_APP=service

RUN pip install -r requirements.txt

USER app
ENTRYPOINT ["flask"]
CMD ["run"]