run-local:
	cd src/hugo_site &&\
	JOB_NAME=sample-hugo-page JOB_VERSION=0.0.1 \
	hugo server -D --port 7000

test-build:
	cd src &&\
	DOCKER_BUILDKIT=1 docker build \
		-t ghcr.io/theracetrack/racetrack/job-base/hugo:latest \
		-f base.Dockerfile .

bundle:
	cd src &&\
	racetrack plugin bundle --out=.. &&\
	racetrack plugin bundle --out=.. --out-filename=latest.zip

install:
	racetrack plugin install --replace latest.zip

deploy-sample:
	racetrack deploy sample
