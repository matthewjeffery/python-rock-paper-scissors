FROM python:3

ENV GUI_ENABLED false

RUN pip install tabulate && pip install tabulate[widechars]

COPY play.py /rock-paper-scissors/

WORKDIR /rock-paper-scissors

ENTRYPOINT ["python", "play.py"]