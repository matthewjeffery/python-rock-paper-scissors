FROM python:3

RUN pip install tabulate

COPY play.py /rock-paper-scissors/

WORKDIR /rock-paper-scissors

ENTRYPOINT ["python", "play.py"]