import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="policy_sentry",
    include_package_data=True,
    version="0.4.4",
    author="Kinnaird McQuade",
    author_email="kinnairdm@gmail.com",
    description="Generate locked-down AWS IAM Policies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salesforce/policy_sentry",
    packages=setuptools.find_packages(),
    install_requires=[
        'click',
        'sqlalchemy',
        'pandas',
        'policyuniverse',
        'PyYAML',
        'bs4',
        'html5lib',
        'lxml',
        'jinja2',
        'schema'
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
    python_requires='>=3.6',
    scripts=['policy_sentry/bin/policy_sentry'],
)
