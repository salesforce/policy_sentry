import json
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class MinifyIAMDataHook(BuildHookInterface):
    """Hatch build hook that minifies the IAM data store before building."""

    PLUGIN_NAME = "minify_iam_data"

    def initialize(self, _version, build_data):
        src = Path("policy_sentry/shared/data/iam-definition.json")
        dest = Path(self.root) / src

        dest.parent.mkdir(parents=True, exist_ok=True)
        minified = json.dumps(json.loads(src.read_bytes()), separators=(",", ":"))
        dest.write_text(minified)
