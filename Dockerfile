FROM python:3

COPY play.py /

RUN pip install tabulate

ENTRYPOINT ["python", "./play.py"]