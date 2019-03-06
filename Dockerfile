FROM python:3

COPY play.py /

ENTRYPOINT ["python", "./play.py"]