from __future__ import annotations
from pathlib import Path


class Plugin:
    def fatman_job_types(self) -> dict[str, list[tuple[Path, Path]]]:
        """
        Job types provided by this plugin
        :return dict of job type name (with version) -> list of images: (base image path, dockerfile template path)
        """
        return {
            f'hugo:{self.plugin_manifest.version}': [
                (self.plugin_dir / 'base-1.Dockerfile', self.plugin_dir / 'fatman-1.Dockerfile'),
                (self.plugin_dir / 'base-2.Dockerfile', self.plugin_dir / 'fatman-2.Dockerfile'),
            ],
        }
