FROM {{ base_image }}

{% if manifest.wrapper_properties and manifest.wrapper_properties['site_title'] %}
RUN sed -i '/title =/s/= .*/= "{{ manifest.wrapper_properties['site_title'] }}"/' /src/hugo_site/config.toml
{% endif %}

COPY . /src/hugo_site/
RUN chmod -R a+rw /src/hugo_site/
