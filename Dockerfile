FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install firefox-geckodriver -y

FROM python:3.11

RUN apt-get update
RUN apt-get install firefox-esr -y
COPY --from=0 /usr/bin/geckodriver /sbin/geckodriver

WORKDIR /app

COPY src/ src/
COPY pickles/ pickles/
COPY requirements.txt ./

RUN mkdir plots

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
