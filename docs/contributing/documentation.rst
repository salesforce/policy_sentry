Contributing to Documentation
=============================

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


Docstrings
~~~~~~~~~~~~~

The comments under each Python Module are Docstrings. We use those to generate our documentation. See more information here: https://sphinx-rtd-tutorial.readthedocs.io/en/latest/build-the-docs.html#generating-documentation-from-docstrings.

Use the Google style for Docstrings, as shown here: http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#google-vs-numpy

::
  def func(arg1, arg2):
    """Summary line.

    Extended description of function.

    Args:
        arg1 (int): Description of arg1
        arg2 (str): Description of arg2

    Returns:
        bool: Description of return value

    """
    return True
