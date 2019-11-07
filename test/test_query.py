import unittest
from pathlib import Path
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.query import query_condition_table_by_name, query_condition_table

HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME
db_session = connect_db(database_file_path)


class QueryTestCase(unittest.TestCase):
    def test_query_condition_table(self):
        """Tests function that grabs a list of condition keys per service."""
        desired_output = [
            'cloud9:EnvironmentId',
            'cloud9:EnvironmentName',
            'cloud9:InstanceType',
            'cloud9:Permissions',
            'cloud9:SubnetId',
            'cloud9:UserArn'
        ]
        output = query_condition_table(db_session, "cloud9")
        self.assertEquals(desired_output, output)

    def test_query_condition_table_by_name(self):
        """Tests function that grabs details about a specific condition key"""
        desired_output = {
            "name": "cloud9:Permissions",
            "description": "Filters access by the type of AWS Cloud9 permissions",
            "condition_value_type": "string"
        }
        output = query_condition_table_by_name(db_session, "cloud9", "cloud9:Permissions")
        self.assertEquals(desired_output, output)

