FROM golang:1.19-alpine

RUN apk add hugo

WORKDIR /src/hugo_site
COPY --from=jobtype  hugo_site/. /src/hugo_site/

CMD hugo server -D --bind 0.0.0.0 --port 7001

EXPOSE 7001
LABEL racetrack-component="job"


{% if manifest.wrapper_properties and manifest.wrapper_properties['site_title'] %}
RUN sed -i '/title =/s/= .*/= "{{ manifest.wrapper_properties['site_title'] }}"/' /src/hugo_site/config.toml
{% endif %}

{% if manifest.jobtype_extra and manifest.jobtype_extra['site_title'] %}
RUN sed -i '/title =/s/= .*/= "{{ manifest.jobtype_extra['site_title'] }}"/' /src/hugo_site/config.toml
{% endif %}

COPY . /src/hugo_site/
RUN chmod -R a+rw /src/hugo_site/
