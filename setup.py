"""Setup script for Policy Sentry"""
import setuptools
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')
TESTS_REQUIRE = [
    'coverage',
    'pytest'
]
REQUIRED_PACKAGES = [
    'beautifulsoup4',
    'click',
    'requests',
    'schema',
    'PyYAML',
]
PROJECT_URLS = {
    "Documentation": "https://policy-sentry.readthedocs.io/",
    "Code": "https://github.com/salesforce/policy_sentry/",
    "Twitter": "https://twitter.com/kmcquade3",
    "Red Team Report": "https://opensource.salesforce.com/policy_sentry"
}


def get_version():
    init = open(
        os.path.join(
            HERE,
            "policy_sentry",
            "bin",
            "version.py"
        )
    ).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


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
    packages=setuptools.find_packages(exclude=['test*']),
    tests_require=TESTS_REQUIRE,
    install_requires=REQUIRED_PACKAGES,
    project_urls=PROJECT_URLS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    entry_points={"console_scripts": "policy_sentry=policy_sentry.bin.cli:main"},
    zip_safe=True,
    keywords='aws iam roles policy policies privileges security',
    python_requires='>=3.6',
)
