FROM {{ base_image }}

ENV JOB_NAME "{{ manifest.name }}"
ENV JOB_VERSION "{{ manifest.version }}"
ENV GIT_VERSION "{{ git_version }}"
ENV DEPLOYED_BY_RACETRACK_VERSION "{{ deployed_by_racetrack_version }}"
