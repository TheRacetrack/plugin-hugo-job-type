FROM {{ base_image }}

{% for env_key, env_value in env_vars.items() %}
ENV {{ env_key }} "{{ env_value }}"
{% endfor %}

{% if manifest.system_dependencies and manifest.system_dependencies|length > 0 %}
RUN apk add \
    {{ manifest.system_dependencies | join(' ') }}
{% endif %}

{% if manifest.golang.gomod %}
COPY "{{ manifest.golang.gomod }}" /src/fatman/
RUN cd /src/fatman && go mod download
{% endif %}

COPY . /src/go_wrapper/handler/
RUN chmod -R a+rw /src/go_wrapper && cd /src/go_wrapper/ && go mod download

RUN go get ./... && go build -o go_wrapper

ENV FATMAN_NAME "{{ manifest.name }}"
ENV FATMAN_VERSION "{{ manifest.version }}"
ENV GIT_VERSION "{{ git_version }}"
ENV DEPLOYED_BY_RACETRACK_VERSION "{{ deployed_by_racetrack_version }}"
