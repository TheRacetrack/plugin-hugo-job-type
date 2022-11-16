FROM golang:1.19-alpine

RUN apk add hugo

WORKDIR /src/hugo_wrapper

COPY hugo_wrapper/. /src/hugo_wrapper/
RUN go get ./... && rm -rf /src/hugo_wrapper/handler

CMD ./hugo_wrapper < /dev/null
LABEL racetrack-component="fatman"
