ARG FROM_TAG=3.7-slim-buster
FROM python:${FROM_TAG}
MAINTAINER Kinnaird McQuade "kinnairdm@gmail.com"

# Install python dependencies
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt --no-cache-dir && \
    rm -rf /root/.cache/

COPY . /tmp/policy_sentry
RUN pip install /tmp/policy_sentry --no-cache-dir && \
    rm -rf /root/.cache/

# Allow the container to accept arguments
COPY ./utils/entrypoint.sh /usr/bin/entrypoint.sh

ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]
CMD ["--help"]
