import unittest
from policy_sentry.writing.sid_group import SidGroup


class TestMinimizeWrite(unittest.TestCase):
    def test_minimize_rw_same(self):
        cfg = {
            "mode": "crud",
            "name": "",
            "read": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
            ],
            "write": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
            ]
        }
        sid_grp = SidGroup()
        write_format = sid_grp.process_template(cfg,minimize=1)
        write_format.pop('Version')
        self.assertEqual(len(write_format['Statement']), 1, "More than one statement returned, expected 1")
        expected_action = ['ssm:getpar*','ssm:deletepar*','ssm:la*','ssm:putp*']
        self.assertEqual(write_format['Statement'][0]['Action'], expected_action, "extra actions are returned")
        self.assertEqual(write_format['Statement'][0]['Resource'], cfg['read'], "Wrong resources were returned")

    def test_minimize_rw_different(self):
        cfg = {
            "mode": "crud",
            "name": "",
            "read": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
            ],
            "write": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter10"
            ]
        }
        sid_grp = SidGroup()
        write_format = sid_grp.process_template(cfg,minimize=1)
        write_format.pop('Version')
        self.assertEqual(len(write_format['Statement']), 2, "More than one statement returned, expected 1")
        self.assertEqual(write_format['Statement'][0]['Action'], ['ssm:getpar*'], "extra actions are returned")
        self.assertEqual(write_format['Statement'][0]['Resource'], cfg['read'], "Wrong resources were returned")
        self.assertEqual(write_format['Statement'][1]['Action'], ['ssm:deletepar*', 'ssm:la*', 'ssm:putp*'],
                         "extra actions are returned")
        self.assertEqual(write_format['Statement'][1]['Resource'], cfg['write'], "Wrong resources were returned")

if __name__ == '__main__':
    unittest.main()
