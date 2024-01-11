FROM python:3.9-slim-bullseye

WORKDIR /src/proxy_wrapper

COPY --from=jobtype proxy_wrapper/requirements.txt /src/proxy_wrapper/
RUN pip install -r /src/proxy_wrapper/requirements.txt

COPY --from=jobtype  proxy_wrapper/proxy_wrapper/. /src/proxy_wrapper/proxy_wrapper/

CMD python -u -m proxy_wrapper.main run
LABEL racetrack-component="job"


ENV JOB_NAME "{{ manifest.name }}"
ENV JOB_VERSION "{{ manifest.version }}"
ENV GIT_VERSION "{{ git_version }}"
ENV DEPLOYED_BY_RACETRACK_VERSION "{{ deployed_by_racetrack_version }}"
