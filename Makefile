run-local:
	cd hugo-job-type/hugo_wrapper &&\
	FATMAN_NAME=sample-hugo-page FATMAN_VERSION=0.0.1 \
	hugo server -D --port 7000

test-build:
	cd hugo-job-type &&\
	DOCKER_BUILDKIT=1 docker build \
		-t ghcr.io/theracetrack/racetrack/fatman-base/hugo:latest \
		-f base.Dockerfile .

bundle:
	cd hugo-job-type &&\
	racetrack plugin bundle --out=..

deploy-sample:
	racetrack deploy sample-hugo-page docker
