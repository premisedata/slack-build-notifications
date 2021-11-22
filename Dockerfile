FROM python:3.9.7-slim-buster

RUN pip install slack_sdk

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python3", "/entrypoint.py"]
