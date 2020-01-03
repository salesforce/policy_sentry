ARG FROM_TAG=3.7
FROM python:${FROM_TAG}
MAINTAINER Kinnaird McQuade "kinnairdm@gmail.com"

# Install python dependencies
RUN pip install pipenv
COPY ./Pipfile* /tmp/
# Use Pipfile to generate requirements.txt and install those dependencies
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/policy_sentry
RUN pip install /tmp/policy_sentry
RUN /usr/local/bin/policy_sentry initialize

# Allow the container to accept arguments
COPY ./utils/entrypoint.sh /usr/bin/entrypoint.sh

ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]
CMD ["--help"]
