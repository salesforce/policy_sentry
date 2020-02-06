Docker
##################

If you prefer using Docker instead of installing the script with Python, we support that as well.

Use this to build the docker image:

.. code-block:: bash

    docker build -t kmcquade/policy_sentry .


Use this to run some basic commands:

.. code-block:: bash

    # Basic commands with no arguments
    docker run -i --rm kmcquade/policy_sentry:latest "--help"
    docker run -i --rm kmcquade/policy_sentry:latest "query"

    # Query the database
    docker run -i --rm kmcquade/policy_sentry:latest "query action-table --service all --access-level permissions-management"


The `write-policy` command also supports passing in the YML config via STDIN. Try it out here:

.. code-block:: bash

    # Write policies by passing in the config via STDIN
    cat examples/yml/crud.yml | docker run -i --rm kmcquade/policy_sentry:latest "write-policy"
    cat examples/yml/actions.yml | docker run -i --rm kmcquade/policy_sentry:latest "write-policy"
