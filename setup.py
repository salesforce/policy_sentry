import setuptools
import os
import re

HERE = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')
TESTS_REQUIRE = [
    'coverage',
    'nose',
    'pytest'
]


def get_version():
    init = open(os.path.join(HERE, 'policy_sentry/bin/', 'policy_sentry')).read()
    return VERSION_RE.search(init).group(1)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="policy_sentry",
    include_package_data=True,
    version=get_version(),
    author="Kinnaird McQuade",
    author_email="kinnairdm@gmail.com",
    description="Generate locked-down AWS IAM Policies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salesforce/policy_sentry",
    packages=setuptools.find_packages(exclude=['test*']),
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'click',
        'sqlalchemy',
        'pandas',
        'policyuniverse',
        'PyYAML',
        'beautifulsoup4',
        'html5lib',
        'lxml',
        'jinja2',
        'requests',
        'schema',
        'click_log'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # entry_points='''
    #     [console_scripts]
    #     policy_sentry=policy_sentry.bin:policy_sentry
    # ''',
    keywords='aws iam roles policy policies privileges security',
    python_requires='>=3.6',
    scripts=['policy_sentry/bin/policy_sentry'],
)
