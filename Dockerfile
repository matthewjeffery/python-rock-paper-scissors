FROM python:3

RUN pip install tabulate && pip install tabulate[widechars]

COPY play.py /rock-paper-scissors/

WORKDIR /rock-paper-scissors

ENTRYPOINT ["python", "play.py"]