class Plugin:
    def job_types(self) -> dict[str, dict]:
        """
        Job types provided by this plugin
        """
        plugin_version: str = getattr(self, 'plugin_manifest').version
        return {
            f'hugo:{plugin_version}': {
                'images': [
                    {
                        'source': 'jobtype',
                        'dockerfile_path': 'job-1.Dockerfile',
                        'template': True,
                    },
                    {
                        'source': 'jobtype',
                        'dockerfile_path': 'job-2.Dockerfile',
                        'template': True,
                    },
                ],
            },
        }
