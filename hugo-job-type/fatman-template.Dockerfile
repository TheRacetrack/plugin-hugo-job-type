FROM {{ base_image }}

{% for env_key, env_value in env_vars.items() %}
ENV {{ env_key }} "{{ env_value }}"
{% endfor %}

{% if manifest.system_dependencies and manifest.system_dependencies|length > 0 %}
RUN apk add \
    {{ manifest.system_dependencies | join(' ') }}
{% endif %}


ENV FATMAN_NAME "{{ manifest.name }}"
ENV FATMAN_VERSION "{{ manifest.version }}"
ENV GIT_VERSION "{{ git_version }}"
ENV DEPLOYED_BY_RACETRACK_VERSION "{{ deployed_by_racetrack_version }}"
