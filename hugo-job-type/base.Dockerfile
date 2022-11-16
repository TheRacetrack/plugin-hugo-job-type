FROM golang:1.19-alpine

RUN apk add hugo

WORKDIR /src/hugo_wrapper

COPY hugo_wrapper/. /src/hugo_wrapper/

CMD hugo server -D --port 7000
LABEL racetrack-component="fatman"
