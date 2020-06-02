from policy_sentry.shared import constants

constants.CONFIG_DIRECTORY = "/tmp/.policy_sentry"
constants.LOCAL_DATASTORE_FILE_PATH = "/tmp/.policy_sentry/iam-definition.json"
constants.LOCAL_ACCESS_OVERRIDES_FILE = "/tmp/.policy_sentry/access-level-overrides.yml"
constants.LOCAL_HTML_DIRECTORY_PATH = "/tmp/.policy_sentry/data/docs"

from policy_sentry.command.initialize import initialize

if __name__ == '__main__':
    initialize(None, True, True)
