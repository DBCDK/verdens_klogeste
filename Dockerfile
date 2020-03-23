FROM docker.dbc.dk/dbc-python3

RUN useradd -m python

USER python
WORKDIR /home/python

ENV PATH=/home/python/.local/bin:$PATH

COPY --chown=python src src
COPY --chown=python setup.py setup.py

RUN pip install --user .

CMD ["verdens-klogeste-service", "-p", "5000"]

EXPOSE 5000

LABEL AUTHKEY api key for accessing this service
LABEL WATSON_DISCOVERY_APIKEY api key for watson discovery
LABEL WATSON_DISCOVERY_URL url for watson discovery service
LABEL WATSON_NLU_APIKEY api key for watson nlu
LABEL WATSON_NLU_URL url for watson nlu service
