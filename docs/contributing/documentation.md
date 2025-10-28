Contributing to Documentation
=============================

If you're looking to help document Policy Sentry, your first step is to
get set up with Mkdocs, our documentation tool. First you will want to
make sure you have a few things on your local system:

-   python-dev (if you're on OS X, you already have this)
-   [uv](https://docs.astral.sh/uv/getting-started/installation/)

Once you've got all that, the rest is simple:

```bash
# If you have a fork, you'll want to clone it instead
git clone git@github.com:salesforce/policy_sentry.git

# Set up the virtual environment
uv sync --frozen --all-groups

# Create the HTML files
just build-docs
just serve-docs

# The above will open the built documentation in your browser
```

Docstrings
----------

The comments under each Python Module are Docstrings. We use those to
generate our documentation. See more information [here](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/build-the-docs.html#generating-documentation-from-docstrings).

Use the Google style for Docstrings, as shown [here](http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#google-vs-numpy)

```python
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
```
