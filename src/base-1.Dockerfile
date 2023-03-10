FROM python:3.9-slim-bullseye

WORKDIR /src/proxy_wrapper

COPY proxy_wrapper/requirements.txt /src/proxy_wrapper/
RUN pip install -r /src/proxy_wrapper/requirements.txt

COPY proxy_wrapper/proxy_wrapper/. /src/proxy_wrapper/proxy_wrapper/

CMD python -u -m proxy_wrapper.main run
LABEL racetrack-component="job"
