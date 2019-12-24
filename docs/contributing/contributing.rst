Contributing
============

Want to contribute back to Policy Sentry? This page describes the general development
flow, our philosophy, the test suite, and issue tracking.

Impostor Syndrome Disclaimer
----------------------------

Before we get into the details: **We want your help. No, really.**

There may be a little voice inside your head that is telling you that you're
not ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you -- the little voice in your head is wrong. If you can write code
at all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect
code isn't the measure of a good developer (that would disqualify all of us!);
it's trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve.

We've provided some clear `Contribution Guidelines`_ that you can read below.
The guidelines outline the process that you'll need to follow to get a patch
merged. By making expectations and process explicit, we hope it will make it
easier for you to contribute.

And you don't just have to write code. You can help out by writing
documentation, tests, or even by giving feedback about this work. (And yes,
that includes giving feedback about the contribution guidelines.)

(`Adrienne Friend`_ came up with this disclaimer language.)

.. _Adrienne Friend: https://github.com/adriennefriend/imposter-syndrome-disclaimer


Documentation
-------------

If you're looking to help document Policy Sentry, your first step is to get set up with Sphinx, our documentation tool. First you will want to make sure you have a few things on your local system:

* python-dev (if you're on OS X, you already have this)
* pip
* pipenv

Once you've got all that, the rest is simple:

::

    # If you have a fork, you'll want to clone it instead
    git clone git@github.com:salesforce/policy_sentry.git

    # Set up the Pipenv
    pipenv install --skip-lock
    pipenv shell

    # Enter the docs directory and compile
    cd docs/
    make html

    # View the file titled docs/_build/html/index.html in your browser



Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

Inside the ``docs`` directory, you can run ``make`` to build the documentation.
See ``make help`` for available options and the `Sphinx Documentation
<http://sphinx-doc.org/contents.html>`_ for more information.



Developing Locally
-----------------------


Pipenv
~~~~~~

.. code-block:: bash

   pipenv --python 3.7  # create the environment
   pipenv shell         # start the environment
   pipenv install       # install both development and production dependencies



Updating the AWS HTML files
----------------------------

This will update the HTML files stored in `policy_sentry/shared/data/docs/list_*.partial.html`

.. code-block:: bash
   python3 ./utils/download_docs.py

This downloads the Actions, Resources, and Condition Keys pages per-service to the ``policy_sentry/shared/data/docs`` folder. It also add a file titled ``policy_sentry/shared/links.yml`` as well.

When a user runs ``policy_sentry initialize``, these files are copied over to the config folder (``~/.policy_sentry/``).

This design choice was made for a few reasons:

1. **Don't break because of AWS**: The automation must **not** break if the AWS website is down, or if AWS drastically changes the documentation.
2. **Replicability**: Two ``git clones`` that build the SQLite database should always have the same results
3. **Easy to review**: The repository itself should contain easy-to-understand and easy-to-view documentation, which the user can replicate, to verify with the human eye that no malicious changes have been made.
    - This means no JSON files with complicated structures, or Binary files (the latter of which does not permit ``git diff``s) in the repository.
    - This helps to mitigate the concern that open source software could be modified to alter IAM permissions at other organizations.


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
