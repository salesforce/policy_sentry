"""Setup script for Policy Sentry"""

import json
import re
from pathlib import Path

import setuptools
from setuptools.command.build_py import build_py

HERE = Path(__file__).parent
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
TESTS_REQUIRE = ["coverage", "pytest"]
REQUIRED_PACKAGES = [
    "beautifulsoup4",
    "click",
    "requests",
    "schema",
    "PyYAML",
    "orjson",
]
PROJECT_URLS = {
    "Documentation": "https://policy-sentry.readthedocs.io/",
    "Code": "https://github.com/salesforce/policy_sentry/",
    "Twitter": "https://twitter.com/kmcquade3",
    "Red Team Report": "https://opensource.salesforce.com/policy_sentry",
}


class PreBuildCommand(build_py):
    """Pre-build command"""

    def minify_iam_data_json(self) -> None:
        """Minifies the IAM DB JSON file"""
        src_iam_data_path = Path("policy_sentry/shared/data/iam-definition.json")
        build_iam_data_path = Path(self.build_lib) / src_iam_data_path

        self.mkpath(str(build_iam_data_path.parent))
        minified = json.dumps(json.loads(src_iam_data_path.read_bytes()), separators=(",", ":"))
        build_iam_data_path.write_text(minified)

    def run(self) -> None:
        self.execute(self.minify_iam_data_json, ())
        build_py.run(self)


def get_version() -> str:
    init = (HERE / "policy_sentry/bin/version.py").read_text()
    return VERSION_RE.search(init).group(1)


def get_description() -> str:
    (HERE / "README.md").read_text()


setuptools.setup(
    name="policy_sentry",
    include_package_data=True,
    version=get_version(),
    author="Kinnaird McQuade",
    author_email="kinnairdm@gmail.com",
    description="Generate locked-down AWS IAM Policies",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/salesforce/policy_sentry",
    packages=setuptools.find_packages(exclude=["test*"]),
    package_data={
        "policy_sentry": ["py.typed"],
        "policy_sentry.shared": [
            "data/*.json",
            "data/*.yml",
            "data/audit/*.txt",
        ],
    },
    tests_require=TESTS_REQUIRE,
    install_requires=REQUIRED_PACKAGES,
    project_urls=PROJECT_URLS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Typing :: Typed",
    ],
    entry_points={"console_scripts": "policy_sentry=policy_sentry.bin.cli:main"},
    zip_safe=True,
    keywords="aws iam roles policy policies privileges security",
    python_requires=">=3.9",
    cmdclass={
        "build_py": PreBuildCommand,
    },
)
