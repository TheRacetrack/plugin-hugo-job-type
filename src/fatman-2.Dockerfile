FROM {{ base_image }}

COPY . /src/hugo_site/
RUN chmod -R a+rw /src/hugo_site/
