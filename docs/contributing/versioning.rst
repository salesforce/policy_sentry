Versioning
--------------------

We try to follow `Semantic Versioning <https://semver.org/>`__ as much as possible.


Version bumps
--------------

Just edit the `policy_sentry/bin/policy_sentry` file and update the `__version__` variable:

.. code-block:: python

    #! /usr/bin/env python
    """
        policy_sentry is a tool for generating least-privilege IAM Policies.
    """
    __version__ = '0.6.3'  # EDIT THIS

The `setup.py` file will automatically pick up the new version from that file for the package info. The `@click.version_option` decorator will also pick that up for the command line.
