from __future__ import annotations
from pathlib import Path


class Plugin:
    def job_types(self) -> dict[str, list[tuple[Path, Path]]]:
        """
        Job types provided by this plugin
        :return dict of job type name (with version) -> list of images: (base image path, dockerfile template path)
        """
        return {
            f'hugo:{self.plugin_manifest.version}': [
                (self.plugin_dir / 'base-1.Dockerfile', self.plugin_dir / 'job-1.Dockerfile'),
                (self.plugin_dir / 'base-2.Dockerfile', self.plugin_dir / 'job-2.Dockerfile'),
            ],
        }
