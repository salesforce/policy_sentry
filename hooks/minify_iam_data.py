import json
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

IAM_DATA_PATH = Path("policy_sentry/shared/data/iam-definition.json")


class MinifyIAMDataHook(BuildHookInterface):
    """Hatch build hook that minifies the IAM data store before building."""

    PLUGIN_NAME = "minify_iam_data"

    def initialize(self, _version, _build_data):
        dest = Path(self.root) / IAM_DATA_PATH

        dest.parent.mkdir(parents=True, exist_ok=True)
        minified = json.dumps(json.loads(IAM_DATA_PATH.read_bytes()), separators=(",", ":"))
        dest.write_text(minified)

    def finalize(self, _version, _build_data, _artifact_path):
        # after the build, pretty format the json file again
        file_path = Path(self.root) / IAM_DATA_PATH
        file_path.write_text(json.dumps(json.loads(file_path.read_bytes()), indent=2))
