# Racetrack Plugin: HUGO Job Type

This is a plugin for [Racetrack](https://github.com/TheRacetrack/racetrack)
which extends it with [HUGO framework](https://gohugo.io/) Job Type.
It's a language wrapper converting your code compatible with HUGO standards to a Fatman web service.

## Setup
1. Install `racetrack` client and generate ZIP plugin by running `make bundle`.

2. Activate the plugin in Racetrack Dashboard Admin page
  by uploading the zipped plugin file.

## Usage
You can deploy sample HUGO job by running:
```bash
racetrack deploy sample
```

See the [example](./sample).
